#!/bin/env python
################################################################
import argparse
import base64
import fnmatch
import os
from typing import TYPE_CHECKING

from datasize import DataSize

from solidipes.loaders.file import File
from solidipes.loaders.file_sequence import FileSequence
from solidipes.loaders.mime_types import extension2mime_type, is_valid_extension, mime_types2extensions
from solidipes.loaders.sequence import Sequence
from solidipes.reports.report import Report
from solidipes.scanners.scanner import Scanner, StreamlitProgressBar, list_files
from solidipes.utils import get_git_repository, get_git_root, get_mimes, get_study_metadata, logging, set_mimes
from solidipes.utils.git_infos import GitInfos

if TYPE_CHECKING:
    import streamlit as st
else:
    import lazy_loader as lazy

    st = lazy.load("streamlit")

print = logging.invalidPrint
logger = logging.getLogger()
jupyter_icon_filename = os.path.join(os.path.dirname(__file__), "jupyter_logo.png")
_jupyter_icon = base64.b64encode(open(jupyter_icon_filename, "rb").read()).decode("utf-8")


def transform_to_subtree(h, subtree=""):
    tree = []
    for name, f in h.items():
        if isinstance(f, dict):
            current_dir = os.path.join(subtree, name)
            s = transform_to_subtree(f, current_dir)
            if s:
                tree.append({"label": name, "value": current_dir, "children": s})
            else:
                tree.append({"label": name, "value": current_dir})
    return tree


################################################################


class StateWrapper:
    def __init__(self, f):
        self.key = "solidipes_state_GUI_" + f.unique_identifier
        self.f = f
        if "GUI_files" not in st.session_state:
            st.session_state["GUI_files"] = {}
        if self.key not in st.session_state["GUI_files"]:
            st.session_state["GUI_files"][self.key] = {}

    def __getattribute__(self, name):
        if name in ["key", "f"]:
            return super().__getattribute__(name)

        try:
            if name not in st.session_state["GUI_files"][self.key]:
                st.session_state["GUI_files"][self.key][name] = None
            return st.session_state["GUI_files"][self.key][name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        if name in ["key", "f"]:
            super().__setattr__(name, value)
            return

        try:
            if self.key not in st.session_state["GUI_files"]:
                st.session_state["GUI_files"][self.key] = {}
            st.session_state["GUI_files"][self.key][name] = value
        except KeyError:
            pass


################################################################


class FileWrapper:
    def __init__(self, f):
        self.state = StateWrapper(f)
        self.f = f

    def __getattr__(self, name):
        if name in ["state", "f"]:
            return super().__getattr__(name)

        return getattr(self.f, name)


################################################################


class WebReport:
    def __init__(self):
        self.git_infos = GitInfos()
        self.display_push_button = False
        self.file_wildcard = "*"
        self.file_error_checkbox = None
        self.scanner = Scanner()
        st.set_page_config(layout="wide", page_icon="https://gitlab.com/dcsm/website/-/raw/main/static/favicon.ico")
        if "currently_opened" not in st.session_state:
            st.session_state["currently_opened"] = None

        self.createLayouts()

    def createLayouts(self):
        from solidipes.reports.widgets.gitlab_issues import GitlabIssues
        from solidipes.reports.widgets.zenodo import ZenodoInfos, ZenodoPublish

        self.progress_layout = st.sidebar.empty()

        st.sidebar.markdown("*Powered by* **Solidipes**")
        st.sidebar.markdown(
            '<center><img src="https://gitlab.com/dcsm/solidipes/-/raw/main/logos/solidipes.jpg" width="60%"'
            ' style="border-radius:50%;" /><br><a style="font-size: 13px;"'
            ' href="https://gitlab.com/dcsm/solidipes">https://gitlab.com/dcsm/solidipes</a></center>',
            unsafe_allow_html=True,
        )
        st.sidebar.markdown(
            '<p style="font-size: 10px"><center><em>Software funded by</em> <img width="100px"'
            ' src="https://ethrat.ch/wp-content/uploads/2021/12/ethr_en_rgb_black.svg"/>&nbsp;'
            '<a style="font-size: 10px" href="https://ethrat.ch/en/">https://ethrat.ch/en/</a></center></p>',
            unsafe_allow_html=True,
        )
        st.sidebar.markdown("---")
        self.gitlab_control = st.sidebar.container()
        self.jupyter_control = st.sidebar.container()
        self.filebrowser_control = st.sidebar.container()
        self.update_buttons = st.sidebar.container()
        self.file_selector = st.sidebar.container()
        self.path_selector = st.sidebar.container()
        if self.git_infos.repository is not None:
            self.git_control = st.sidebar.container()
        self.env_layout = st.sidebar.container()
        self.options = st.sidebar.expander("Options")

        self.main_layout = st.container()
        self.file_layout = st.container()
        # self.modified_state = self.main_layout.empty()
        self.global_message = self.main_layout.container()
        self.header_layout = self.main_layout.container()
        self.tab_metadata, self.tab_files = self.main_layout.container(), self.main_layout.container()
        self.zenodo_publish = ZenodoPublish(self.tab_metadata, self.global_message, self.progress_layout)
        self.zenodo_infos = ZenodoInfos(self.tab_metadata)
        if self.git_infos.origin is not None:
            self.gitlab_issues = GitlabIssues(self.main_layout)
        self.files_container = self.main_layout.container()
        self.logs = self.main_layout.container()

    def alternative_parser(self, e):
        return []

    def get_file_title(self, e):
        path = e.file_info.path
        if isinstance(e.f, FileSequence):
            path = e.f.path

        file_title = f"{path}"

        if isinstance(e.f, FileSequence):
            file_size = e.total_size
        else:
            file_size = e.file_info.size

        file_title += f"&nbsp; &nbsp; **{e.file_info.type.strip()}/{DataSize(file_size):.2a}** "
        title = file_title

        if e.state.valid and (not e.discussions or e.archived_discussions):
            title = ":white_check_mark: &nbsp; &nbsp;" + file_title
        else:
            title = ":no_entry_sign: &nbsp; &nbsp; " + file_title

        # if e.discussions or e.state.view:
        #    title += "&nbsp; :arrow_forward: &nbsp; &nbsp; "

        if e.state.view:
            title += "&nbsp; :open_book:"

        if e.discussions:
            title += "&nbsp;:e-mail: &nbsp; :arrow_forward: **You have a message**"

        return title

    def get_file_edit_link(self, e):
        _path = e.file_info.path
        while os.path.islink(_path):
            dirname = os.path.dirname(_path)
            _path = os.path.join(dirname, os.readlink(_path))

        url = self.git_infos.origin + "/-/edit/master/data/" + _path
        return url

    def mime_type_information(self, e, layout, main_layout):
        valid_ext = is_valid_extension(e.file_info.path, e.file_info.type)
        if not e.state.valid and not valid_ext:
            type_choice_box = layout.empty()
            type_choice = type_choice_box.container()
            sel = type_choice.radio(
                "Type selection",
                options=["extension", "mime"],
                key="type_sel_" + e.unique_identifier,
                horizontal=True,
            )

            choice = None
            if sel == "mime":
                possible_types = [e for e in mime_types2extensions.keys()]
                choice = type_choice.selectbox(
                    "type",
                    ["Select type"] + possible_types,
                    key="mime_" + e.unique_identifier,
                )
            else:

                def format_types(x):
                    if x == "Select type":
                        return x
                    return f"{x} ({extension2mime_type[x]})"

                possible_types = [e for e in extension2mime_type.keys()]
                choice = type_choice.selectbox(
                    "extension",
                    ["Select type"] + possible_types,
                    format_func=format_types,
                    key="mime_" + e.unique_identifier,
                )
                if choice != "Select type":
                    choice = extension2mime_type[choice]

            if choice != "Select type":
                st.write(choice)
                confirm = main_layout.button(
                    f"Confirm change type {choice} -> {mime_types2extensions[choice]}",
                    type="primary",
                    use_container_width=True,
                )
                if confirm:
                    mimes = get_mimes()
                    mimes[e.file_info.path] = choice
                    set_mimes(mimes)
                    e.clear_cached_metadata(["file_info", "valid_loading"])
                    self.clear_session_state()
                    st.experimental_rerun()
        else:
            layout.info(e.file_info.type)

    def show_file(self, e):
        if not e.state.valid and e.errors:
            for err in e.errors:
                st.error(err)

        def close_file():
            st.session_state["currently_opened"] = None

        st.sidebar.button(
            "&#8629; Back to file list",
            key=f"close_button_{e.unique_identifier}",
            on_click=close_file,
            use_container_width=True,
            type="primary",
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        self.show_discussions(e)

        if e.state.adding_comment:
            from streamlit_ace import st_ace

            content = st_ace(
                theme="textmate",
                show_gutter=False,
                key=f"chat_input_{e.unique_identifier}",
            )
            if content:
                import re

                m = re.match(r"(\w+):(.*)", content)
                if m:
                    e.add_message(m[1], m[2].strip())
                else:
                    e.add_message("Unknown", content)
                e.state.adding_comment = False
                st.experimental_rerun()

        if isinstance(e.f, Sequence):
            sequence_switcher = st.container()
            with sequence_switcher:
                st.write(f"Sequence of {e._element_count} elements.")

                selected_element = st.slider(
                    "Current element",
                    min_value=1,
                    max_value=e._element_count,
                    step=1,
                    key="sequence_switcher_" + e.unique_identifier,
                )
                e.select_element(selected_element - 1, False)

        file_size = e.file_info.size

        col4.download_button(
            f"Download {os.path.basename(e.file_info.path)} ({DataSize(file_size):.2a})",
            data=open(e.file_info.path, "rb"),
            file_name=os.path.basename(e.file_info.path),
            key="download_" + e.unique_identifier,
        )
        try:
            _link = self._get_jupyter_link()
            _link += "/" + os.path.dirname(e.file_info.path)
            col2.markdown(
                f"[Edit in Jupyterlab]({_link}/)",
                unsafe_allow_html=True,
            )
            _link = self._get_filebrowser_link()
            _link += "/" + os.path.dirname(e.file_info.path)
            col2.markdown(
                f"[Edit in Filebrowser]({_link}/)",
                unsafe_allow_html=True,
            )
        except RuntimeError:
            pass

        col3.button(
            ":speech_balloon: add a comment",
            on_click=lambda: setattr(e.state, "adding_comment", True),
            key=f"add_comment_button_{e.unique_identifier}",
        )

        self.mime_type_information(e, col1, st.container())
        container_error = st.container()
        with st.container():
            try:
                with st.spinner(f"Loading {e.file_info.path}..."):
                    e.view()
            except Exception as err:
                with container_error.expander(":warning: Error trying to display file"):
                    st.exception(err)
                    logger.error("Error trying to display file")
                    logger.error(err)
                # raise err

    def display_file(self, e):
        if not fnmatch.fnmatch(e.file_info.path.lower(), self.file_wildcard):
            return

        e.state.valid = e.valid_loading
        if self.file_error_checkbox and e.valid_loading:
            return

        title = self.get_file_title(e)

        if "currently_opened" not in st.session_state:
            st.session_state["currently_opened"] = None

        def open_file_state():
            e.state.view = True
            st.session_state["currently_opened"] = e.unique_identifier

        st.button(f"{title}", use_container_width=True, on_click=open_file_state)
        self.show_discussions(e)

    def show_discussions(self, e):
        from solidipes.reports.widgets.custom_widgets import SpeechBubble

        if not e.discussions:
            return
        if not e.archived_discussions:
            st.markdown("### :speech_balloon: Discussions")
            for author, message in e.discussions:
                SpeechBubble(author, message)
            st.markdown("<br>", unsafe_allow_html=True)

            st.button(
                "Respond",
                on_click=lambda: setattr(e.state, "adding_comment", True),
                key=f"respond_button_{e.unique_identifier}",
            )
            st.markdown("---")

        if self.show_advanced:
            if e.discussions:
                st.markdown("---")
                if not e.archived_discussions:
                    st.button("Archive messages", on_click=e.archive_discussions())
                else:
                    st.button("Unarchive messages", on_click=e.archive_discussions(False))

                st.markdown("---")

    def scan_directories(self, dir_path):
        from streamlit_tree_select import tree_select

        paths_to_explore = []
        all_paths = []
        self._open_in_jupyterlab_button()
        self._open_in_filebrowser_button()
        self._force_rescan_button()

        _st = self.file_selector.expander("File selection tool", expanded=True)
        self.file_wildcard = _st.text_input("File pattern", value=self.file_wildcard)
        self.file_error_checkbox = _st.checkbox("Show only files with errors")

        with st.spinner("Loading directories..."):
            if "scanned_files" not in st.session_state:
                st.session_state["scanned_files"] = {}
                h = self.scanner.get_dirpath_tree()
                s_files = st.session_state["scanned_files"]
                s_files["all_paths"] = self.scanner.get_path_list()
                s_files["nodes"] = transform_to_subtree(h)
            else:
                s_files = st.session_state["scanned_files"]
            nodes = s_files["nodes"]
            all_paths = s_files["all_paths"]
            _st = self.file_selector.expander("Path selection", expanded=True)
            with _st:
                return_select = tree_select(
                    nodes,
                    expanded=all_paths,
                    expand_disabled=True,
                    checked=all_paths,
                )
                paths_to_explore.clear()
                for c in return_select["checked"]:
                    paths_to_explore.append(c)

        return all_paths, paths_to_explore

    def main(self, dir_path):
        self.scanner.root_path = dir_path

        if "GUI_files" not in st.session_state:
            st.session_state["GUI_files"] = {}

        self.show_advanced = False

        if st.session_state["currently_opened"] is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            files_dict = st.session_state["all_found_files_dict"]
            f = files_dict[st.session_state["currently_opened"]]
            with self.file_layout:
                with st.spinner("Loading... please wait"):
                    title = self.get_file_title(f)
                    st.markdown(title)
                    self.show_file(f)
            return

        self.gitlab_control.markdown(
            f"### <center> [View/Edit Gitlab repository]({self.git_infos.origin}) </center>", unsafe_allow_html=True
        )

        self.show_advanced = self.options.checkbox("Advanced", value=False)

        self.zenodo_infos.show()
        if self.show_advanced:
            self.zenodo_publish.show()
        self._environment_info()
        if self.git_infos.repository is not None:
            self._git_info()

        if self.display_push_button:
            changed_files = self.git_get_changed_files()
            if changed_files:
                self.modified_state.button(
                    "Dataset in a modified state: Push Modifications ?",
                    on_click=self.git_push,
                    type="primary",
                    use_container_width=True,
                )
            else:
                self.modified_state.empty()

        if self.git_infos.origin is not None:
            self.gitlab_issues.show()

        st.markdown(
            """
        <style>
        .css-18j515v {
          justify-content: left;
        }
        .css-1umgz6k {
          justify-content: left;
        }
        .ef3psqc12 {
          justify-content: left;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        # st.markdown("---")
        all_paths, selected_paths = self.scan_directories(dir_path)

        if not selected_paths:
            st.markdown("#### Please select a directory on the left panel")
            return

        if "all_found_files" not in st.session_state:
            self.scanner.progress_bar = StreamlitProgressBar("Loading files", self.progress_layout)
            found = self.scanner.get_filtered_loader_tree([p for p in all_paths], recursive=False)
            files = list_files(found)
            files_dict = self.scanner.get_filtered_loader_dict([p for p in all_paths], recursive=False)
            files_dict = {k: FileWrapper(v) for k, v in files_dict.items()}
            st.session_state["all_found_files"] = files
            st.session_state["all_found_files_dict"] = files_dict

        all_found_files = st.session_state["all_found_files"]

        if not all_found_files:
            st.markdown(f"#### Nothing in the paths: {selected_paths}")
            return

        with self.tab_files:
            self.display_files(all_found_files, selected_paths)

        if self.show_advanced:
            self.logs.markdown("---")

            with self.logs.expander("Logs"):
                from solidipes.utils import get_study_log_path

                col1, col2 = st.columns(2)
                log_filename = get_study_log_path()

                def refresh():
                    st.experimental_rerun

                def clear_log():
                    open(log_filename, "w").close()
                    refresh()

                col1.button("Refresh", on_click=refresh)
                col2.button("Clear", on_click=clear_log)
                st.code("\n".join(open(log_filename).read().split("\n")[::-1]))

    def _get_jupyter_link(self):
        try:
            session = os.environ["SESSION_URL"]
            dir_path = os.getcwd()
            rel_path = os.path.relpath(dir_path, self.git_infos.root)
            if rel_path == ".":
                _link = f"{session}/lab/"
            else:
                _link = f"{session}/lab/tree/{rel_path}"
            return _link
        except Exception:
            raise RuntimeError("Not in a renku session")

    def _get_filebrowser_link(self):
        try:
            session = os.environ["SESSION_URL"]
            dir_path = os.getcwd()
            rel_path = os.path.relpath(dir_path, self.git_infos.root)
            _link = f"{session}/filebrowser/files/{rel_path}"
            return _link
        except Exception:
            raise RuntimeError("Not in a renku session")

    def _jupyter_link(self, uri, size):
        _img = f'<a href="{uri}"><img height="{size}" src="data:image/png;base64,{_jupyter_icon}"></a>'
        return _img

    def _write_jupyter_link(self):
        try:
            _link = self._get_jupyter_link()
            st.markdown(
                f"### <center>[View/Edit in Jupyterlab]({_link}) </center>",
                unsafe_allow_html=True,
            )
        except Exception as err:
            st.error("Jupyter not accessible: " + str(err))

    def _write_filebrowser_link(self):
        try:
            _link = self._get_filebrowser_link()
            st.markdown(
                f"### <center>[View/Edit with file browser]({_link}) </center>",
                unsafe_allow_html=True,
            )
        except Exception as err:
            st.error("Filebrowser not accessible: " + str(err))

    def display_files(self, files, selected_paths):
        bar = self.progress_layout.progress(0, text="Loading files")

        selected_files = []
        for full_path, f in files:
            if os.path.dirname(full_path) not in selected_paths and full_path not in selected_paths:
                continue
            selected_files.append((full_path, f))

        n_files = len(selected_files)

        for i, (full_path, f) in enumerate(selected_files):
            percent_complete = i * 100 // n_files
            bar.progress(percent_complete + 1, text=f"Loading {full_path}")
            if isinstance(f, File) or isinstance(f, FileSequence):
                f = FileWrapper(f)
                self.display_file(f)
            else:
                self.display_dir(full_path, f)
        self.progress_layout.empty()

    def display_dir(self, d, content):
        import streamlit.components.v1 as components

        found_files = False
        for k, v in content.items():
            if isinstance(v, File):
                if fnmatch.fnmatch(v.file_info.path.lower(), self.file_wildcard):
                    found_files = True

        if found_files:
            components.html(
                '<div style="'
                "padding: 0 1em;"
                "line-height: 4em;"
                "border-radius: .5em;"
                "background-color: #dbeff8;"
                "font-family: 'Source Sans Pro', sans-serif;"
                'color:black;"><h3> &#128193; &nbsp;&nbsp;'
                f"{d} </h3></div>"
            )

        for k, v in content.items():
            if not isinstance(v, File):
                continue

    def _open_in_jupyterlab_button(self):
        with self.jupyter_control:
            self._write_jupyter_link()

    def _open_in_filebrowser_button(self):
        with self.filebrowser_control:
            self._write_filebrowser_link()

    def _environment_info(self):
        with self.env_layout.expander("Environment"):
            table_env = [k for k in os.environ.items()]
            st.dataframe(table_env)

    def _git_info(self):
        with self.git_control.container():
            changed_files = self.git_get_changed_files()
            changed_files = [e for e in changed_files if not e.startswith(".solidipes/cloud/")]
            if changed_files:
                with st.expander("Modified Files", expanded=False):
                    for p in changed_files:
                        st.markdown(f"- {p}")

                    st.button(
                        "Revert Modifications",
                        type="primary",
                        use_container_width=True,
                        on_click=self.git_revert,
                    )

    def git_get_changed_files(self):
        changed_files = []
        if self.git_infos.repository:
            changed_files = [item.a_path for item in self.git_infos.repository.index.diff(None)]
        return changed_files

    def git_revert(self):
        repo = get_git_repository()
        ret = repo.git.reset("--hard")
        logger.info("git revert", ret)
        logger.info("git revert", type(ret))
        logger.info("git revert return", ret)
        logger.info("git revert", ret)
        logger.info("git revert", type(ret))
        logger.info("git revert return", ret)
        zenodo_metadata = get_study_metadata()
        import yaml

        zenodo_content = yaml.safe_dump(zenodo_metadata)
        st.session_state["zenodo_metadata_editor"] = zenodo_content
        logger.info(
            "st.session_state['zenodo_metadata_editor']",
            st.session_state["zenodo_metadata_editor"],
        )
        st.session_state["rewrote_zenodo_content"] = True
        self.clear_session_state()

    def git_push(self):
        import subprocess

        import git

        save_cwd = os.getcwd()
        try:
            os.chdir(get_git_root())
            changed_files = self.git_get_changed_files()
            # changed_files = [os.path.relpath(e, os.getcwd()) for e in changed_files]
            for e in changed_files:
                ret = self.git_infos.repository.git.add(e)
            if ret != "":
                self.global_message.info(ret)

            ret = self.git_infos.repository.git.commit('-m "Automatic update from solidipes interface"')
            if ret != "":
                self.global_message.info(ret)

        except git.GitCommandError as err:
            self.global_message.error(err)
            logger.info(err)
            os.chdir(save_cwd)
            return

        os.chdir(save_cwd)

        p = subprocess.Popen(
            "renku dataset update --delete -c --all --no-remote",
            shell=True,
            stdout=subprocess.PIPE,
        )
        p.wait()
        out, err = p.communicate()

        if not p.returncode == 0:
            self.global_message.error("renku update failed")
            if out is not None:
                self.global_message.error(out.decode())
            if err is not None:
                self.global_message.error(err.decode())
        else:
            self.global_message.info(out.decode())

        try:
            origin = self.git_infos.repository.remotes.origin
            origin.push("master")

        except git.GitCommandError as err:
            self.global_message.error(err)
            return

        self.global_message.success("Update repository complete")

        self.clear_session_state()

    def _force_rescan_button(self):
        rescan_button = self.update_buttons.button("Force folder scan", use_container_width=True, type="primary")

        if rescan_button:
            self.clear_session_state()

    def clear_session_state(self):
        logger.info("Clearing session state")
        keys = [k for k in st.session_state]
        for k in keys:
            del st.session_state[k]
        from solidipes.loaders.cached_metadata import CachedMetadata

        CachedMetadata.close_cached_metadata()


################################################################


class WebReportSpawner(Report):
    command = "web_report"
    command_help = "Launch the web graphical interface"

    def make(self, args: argparse.Namespace):
        import subprocess

        if args.debug:
            os.environ["FULL_SOLIDIPES_LOG"] = "true"
        logger.debug(args.additional_arguments)

        cmd = f"streamlit run {__file__} {' '.join(args.additional_arguments)}"
        logger.warning(cmd)
        subprocess.call(cmd, shell=True, cwd=args.dir_path)

    def populate_arg_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "dir_path",
            nargs="?",
            default=".",
            help="Path to the directory to generate the report for. Defaults to current directory",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Enable debug mode",
        )

        parser.add_argument(
            "additional_arguments",
            nargs=argparse.REMAINDER,
            help="Additional arguments to forward to Streamlit",
        )


################################################################
if __name__ == "__main__":
    from solidipes.utils import logging

    logger.info("starting web_report")
    web_report = WebReport()
    web_report.main("./")
