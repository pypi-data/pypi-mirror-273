import io
import subprocess
import tempfile
import adb_tool_py as adb_tool
import adb_tool_py.ui_node as ui_node


class AdbTool:
    def __init__(self, adb_command: adb_tool.AdbCommand):
        self.adb = adb_command
        self.avt = adb_tool.AdbViewTree(adb_command)

    def __init__(self, adb: str = "adb", serial: str = None):
        self.adb = adb_tool.AdbCommand(adb, adb_tool.AdbDevice(serial))
        self.avt = adb_tool.AdbViewTree(self.adb)

    def query(self, cmd: str, stdout=subprocess.PIPE, stderr=subprocess.PIPE) -> subprocess.Popen:
        return self.adb.query(cmd, stdout, stderr)

    def query_async(self, cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) -> subprocess.Popen:
        return self.adb.query_async(cmd, stdout, stderr)

    def logcat(self, output_file=None, cmd: str = '') -> tuple[subprocess.Popen, io.TextIOWrapper]:
        if output_file is None:
            output_file = tempfile.NamedTemporaryFile(delete=False)
        return self.query_async(['logcat', *(cmd.split(' '))], stdout=output_file), output_file

    def logcat_clear(self, cmd: str = '') -> str:
        return self.query(['logcat', '-c', *(cmd.split(' '))])

    def logcat_dump(self, cmd: str = '') -> str:
        return self.query(['logcat', '-d', *(cmd.split(' '))])

    def capture(self) -> None:
        self.avt.capture()

    def content_tree(self) -> ui_node.UINode:
        return self.avt.content_tree

    def find_text(self, text: str, index: int = 0, root_node: ui_node.UINode = None, is_capture: bool = False) -> ui_node.UINode:
        return self.avt.find_text(text, index, root_node, is_capture)

    def find_resource_id(self, resource_id: str, index: int = 0, root_node: ui_node.UINode = None, is_capture: bool = False) -> ui_node.UINode:
        return self.avt.find_resource_id(resource_id, index, root_node, is_capture)

    def check_text(self, text: str, index: int = 0, root_node: ui_node.UINode = None, is_capture: bool = False) -> bool:
        return self.avt.check_text(text, index, root_node, is_capture)

    def check_resource_id(self, resource_id: str, index: int = 0, root_node: ui_node.UINode = None, is_capture: bool = False) -> bool:
        return self.avt.check_resource_id(resource_id, index, root_node, is_capture)

    def touch_text(self, text: str, index: int = 0, root_node: ui_node.UINode = None, is_capture: bool = False) -> bool:
        return self.avt.touch_text(text, index, root_node, is_capture)

    def touch_resource_id(self, resource_id: str, index: int = 0, root_node: ui_node.UINode = None, is_capture: bool = False) -> bool:
        return self.avt.touch_resource_id(resource_id, index, root_node, is_capture)
