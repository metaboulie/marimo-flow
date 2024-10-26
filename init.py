# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "anywidget==0.9.13",
#     "traitlets==5.14.3",
# ]
# ///
"""
This is the starting point for your notebook.
"""

import marimo

__generated_with = "0.9.14"
app = marimo.App()


@app.cell(hide_code=True)
def __(header_widget):
    header_widget
    return


@app.cell(hide_code=True)
def __(mo):
    # Custom Constants
    custom_form = (
        mo.md(
            r"""
            **Customize your constants here:**

            {image}

            """
        )
        .batch(
            image=mo.ui.text(
                value="../assets/<>/<>",
                label="Path of your data: ",
                full_width=True,
            ),  ## add more rows below
        )
        .form(bordered=True, label="Custom Constants")
    )
    custom_form
    return (custom_form,)


@app.cell(hide_code=True)
def __():
    import anywidget
    import traitlets


    class HeaderWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
            const result = model.get("result");

            const container = document.createElement("div");
            container.className = "header-container";

            const banner = document.createElement("img");
            banner.className = "banner";
            banner.src = "https://i.ibb.co/SVcC6bb/final.png";
            banner.style.width = "100%";
            banner.style.height = "200px";
            banner.style.objectFit = "cover";
            banner.style.borderRadius = "10px 10px 0 0";
            banner.alt = "Marimo Banner";

            const form = document.createElement("div");
            form.className = "form-container";

            for (const [key, value] of Object.entries(result)) {
                const row = document.createElement("div");
                row.className = "form-row";

                const label = document.createElement("label");
                label.textContent = key;

                const valueContainer = document.createElement("div");
                valueContainer.className = "value-container";

                if (value.length > 100) {
                    const preview = document.createElement("div");
                    preview.className = "preview";
                    preview.textContent = value.substring(0, 100) + "...";

                    const fullText = document.createElement("div");
                    fullText.className = "full-text";
                    fullText.textContent = value;

                    const toggleButton = document.createElement("button");
                    toggleButton.className = "toggle-button";
                    toggleButton.textContent = "Show More";
                    toggleButton.onclick = () => {
                        if (fullText.style.display === "none") {
                            fullText.style.display = "block";
                            preview.style.display = "none";
                            toggleButton.textContent = "Show Less";
                        } else {
                            fullText.style.display = "none";
                            preview.style.display = "block";
                            toggleButton.textContent = "Show More";
                        }
                    };

                    valueContainer.appendChild(preview);
                    valueContainer.appendChild(fullText);
                    valueContainer.appendChild(toggleButton);

                    fullText.style.display = "none";
                } else {
                    valueContainer.textContent = value;
                }

                row.appendChild(label);
                row.appendChild(valueContainer);
                form.appendChild(row);
            }

            container.appendChild(banner);
            container.appendChild(form);
            el.appendChild(container);
        }
        export default { render };
        """

        _css = """
        .header-container {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            max-width: 100%;
            margin: 0 auto;
            overflow: hidden;
        }

        .banner {
            width: 100%;
            height: auto;
            display: block;
        }

        .form-container {
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            font-weight: 300;
            box-shadow: 0 -10px 20px rgba(0,0,0,0.1);
        }

        .form-row {
            display: flex;
            flex-direction: column;
        }

        label {
            font-size: 0.8em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
            font-weight: 500;
        }

        .value-container {
            font-size: 1em;
            line-height: 1.5;
        }

        .preview, .full-text {
            margin-bottom: 10px;
        }

        .toggle-button {
            border: none;
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .toggle-button:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        @media (max-width: 600px) {
            .form-container {
                grid-template-columns: 1fr;
            }
        }
        """

        result = traitlets.Dict({}).tag(sync=True)
    return HeaderWidget, anywidget, traitlets


@app.cell(hide_code=True)
def __(HeaderWidget):
    header_widget = HeaderWidget(
        result={
            "Title": "My Comprehensive Data Analysis Notebook",
            "Author": "Jane Smith",
            "Date": "2024-09-25",
            "Version": "2.1",
            "Description": "This notebook contains an in-depth analysis of customer behavior patterns across multiple e-commerce platforms. It includes data preprocessing, exploratory data analysis, statistical modeling, and machine learning techniques to derive actionable insights for improving customer engagement and conversion rates.",
            "Keywords": "data analysis, e-commerce, customer behavior, machine learning",
            "Data Sources": "Customer transaction logs, website clickstream data, CRM records, social media interactions",
            "Tools Used": "Python, Pandas, Scikit-learn, Matplotlib, Seaborn, TensorFlow",
        }
    )
    return (header_widget,)


@app.cell(hide_code=True)
def __():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
