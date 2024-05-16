import rio


class RootComponent(rio.Component):
    def build(self) -> rio.Component:
        return rio.Column(
            rio.Text(
                "fooo",
            ),
            rio.Text(
                "fooo",
                style=rio.TextStyle(
                    italic=True,
                ),
            ),
            align_y=0.5,
        )


app = rio.App(
    build=RootComponent,
)

app.run_in_browser()
