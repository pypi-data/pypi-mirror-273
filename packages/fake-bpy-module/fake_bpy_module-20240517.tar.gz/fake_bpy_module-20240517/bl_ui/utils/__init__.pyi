import typing

GenericType = typing.TypeVar("GenericType")

class PresetPanel:
    """ """

    bl_label: typing.Any
    """ """

    bl_region_type: typing.Any
    """ """

    bl_space_type: typing.Any
    """ """

    def draw(self, context):
        """

        :param context:
        """
        ...

    def draw_menu(self, layout, text=None):
        """

        :param layout:
        :param text:
        """
        ...

    def draw_panel_header(self, layout):
        """

        :param layout:
        """
        ...

    def path_menu(
        self,
        searchpaths: list[str],
        operator: str,
        props_default: dict = None,
        prop_filepath: str = "filepath",
        filter_ext: typing.Callable = None,
        filter_path=None,
        display_name: typing.Callable = None,
        add_operator=None,
        add_operator_props=None,
    ):
        """Populate a menu from a list of paths.

                :param searchpaths: Paths to scan.
                :type searchpaths: list[str]
                :param operator: The operator id to use with each file.
                :type operator: str
                :param props_default: Properties to assign to each operator.
                :type props_default: dict
                :param prop_filepath: Optional operator filepath property (defaults to "filepath").
                :type prop_filepath: str
                :param filter_ext: Optional callback that takes the file extensions.

        Returning false excludes the file from the list.
                :type filter_ext: typing.Callable
                :param filter_path:
                :param display_name: Optional callback that takes the full path, returns the name to display.
                :type display_name: typing.Callable
                :param add_operator:
                :param add_operator_props:
        """
        ...
