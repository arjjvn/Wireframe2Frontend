

class LayoutBuilder:

    def __init__(self):
        pass

    # --------------------------------------------------
    # Sort Components
    # --------------------------------------------------

    def sort_components(self, components):
        """
        Sort components from top to bottom,
        then left to right.
        """

        return sorted(
            components,
            key=lambda x: (x["y"], x["x"])
        )

    # --------------------------------------------------
    # Build Layout
    # --------------------------------------------------

    def build(self,
              components,
              framework,
              style,
              theme,
              instruction):

        components = self.sort_components(
            components
        )

        layout = {

            "framework": framework,

            "style": style,

            "theme": theme,

            "instruction": instruction,

            "page": {

                "component_count": len(components),

                "components": components

            }

        }

        return layout

    # --------------------------------------------------
    # Pretty Print
    # --------------------------------------------------

    def pretty(self, layout):

        import json

        return json.dumps(
            layout,
            indent=4
        )