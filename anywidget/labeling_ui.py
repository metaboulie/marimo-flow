import marimo

__generated_with = "0.8.15"
app = marimo.App()


@app.cell(hide_code=True)
def __():
    from openai import OpenAI
    return OpenAI,


@app.cell(hide_code=True)
def __():
    import polars as pl
    return pl,


@app.cell(hide_code=True)
def __():
    import re


    def split_text_into_sentences(text: str, buffer_size: int = 1) -> list[str]:
        """
        Splits text into sentences, adding extra sentences before and after each split based on buffer_size.

        Args:
            text (str): The input text to be split.
            buffer_size (int): Number of sentences to include before and after each split sentence.

        Returns:
            list[str]: List of sentences with additional buffer sentences.
        """
        # Define the regex pattern for sentence splitting
        sentence_pattern = re.compile(
            r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s"
        )

        # Split text into sentences
        sentences = sentence_pattern.split(text)

        # Apply buffer size
        if buffer_size > 0:
            sentences = [
                sentences[i : i + buffer_size * 2 + 1]
                for i in range(max(0, len(sentences) - buffer_size * 2))
            ]

            return [" ".join(chunk).strip() for chunk in sentences]

        return sentences
    return re, split_text_into_sentences


@app.cell(hide_code=True)
def __(buffer_size, split_text_into_sentences, text):
    text_chunked = split_text_into_sentences(text, buffer_size=buffer_size.value)
    return text_chunked,


@app.cell(hide_code=True)
def __():
    # Example usage
    labels = [
        "Strength_rate",
        "Drug",
        "Route",
        "Duration",
        "Frequency",
        "Dosage",
        "Form_form",
        "Date",
        "Strength_amount",
        "Strength_concentration",
        "Time",
    ]
    return labels,


@app.cell(hide_code=True)
def __(generate_label2color, labels):
    label2color = generate_label2color(labels)
    return label2color,


@app.cell
def __(MultiTextAnnotationWidget, label2color, mo, text_chunked):
    widget = mo.ui.anywidget(
        MultiTextAnnotationWidget(
            data=text_chunked, labels=label2color, buffer_size=3
        )
    )
    return widget,


@app.cell(hide_code=True)
def __(mo):
    assist_form = (
        mo.md(
            """
            Copy & Paste the sentence you want OpenAI to assist annotating here

            {user_query}

            Set your OpenAI API Key here

            {api_key}
            """
        ).batch(
            user_query=mo.ui.text_area(
                full_width=True,
            ),
            api_key=mo.ui.text(full_width=True, kind="password"),
        )
    ).form(show_clear_button=True)
    assist_form
    return assist_form,


@app.cell
def __(assist_form, mo, response_df):
    mo.stop(assist_form.value is None)
    response_df
    return


@app.cell
def __(text_chunked):
    text_chunked[0]
    return


@app.cell
def __(mo):
    buffer_size = mo.ui.slider(
        0,
        5,
        1,
        0,
        show_value=True,
        label="buffer size to split text: ",
    )
    buffer_size
    return buffer_size,


@app.cell
def __(widget):
    widget
    return


@app.cell
def __(display_annotations, json, text_chunked, widget):
    result = display_annotations(json.loads(widget.result), text_chunked, False)
    result
    return result,


@app.cell(hide_code=True)
def __(plot_annotation_counts, result):
    plot_annotation_counts(result)
    return


@app.cell(hide_code=True)
def __(pl):
    def display_annotations(
        result: dict[str, list[dict[str, any]]],
        text_data: list[str],
        show_text: bool = True,
    ) -> pl.DataFrame:
        """
        Display annotations from multiple texts in a Polars DataFrame.

        Parameters:
        - result (Dict[str, List[Dict[str, Any]]]): The annotations for each text.
        - text_data (List[str]): The list of texts to be annotated.
        - show_text (bool): Whether to show the text field from the annotations. Default is True.

        Returns:
        - pl.DataFrame: The formatted data as a Polars DataFrame.
        """

        data = []

        for idx, annotations in result.items():
            # Fetch the corresponding text from text_data
            base_text = text_data[int(idx)] if int(idx) < len(text_data) else ""

            # Add the row for the text itself
            if annotations and show_text:
                data.append(
                    {
                        "text": base_text,
                        "token": "",
                        "label": "",
                        "note": "",
                    }
                )
            elif annotations:
                data.append(
                    {
                        "text": f"Text {int(idx) + 1}",
                        "token": "",
                        "label": "",
                        "note": "",
                    }
                )

            for annotation in annotations:
                label = annotation.get("label", "No Label")
                annotated_text = annotation.get("text", "No Text")
                start = annotation.get("start", "N/A")
                end = annotation.get("end", "N/A")
                token = f"{start}-{end}"
                note = annotation.get("note", "No Note")

                # Add a row for each annotation
                data.append(
                    {
                        "text": "",
                        "token": annotated_text,
                        "label": label,
                        "note": note,
                    }
                )

        # Create the Polars DataFrame
        df = pl.DataFrame(data)

        return df
    return display_annotations,


@app.cell(hide_code=True)
def __(pl, px):
    def plot_annotation_counts(df: pl.DataFrame) -> None:
        """
        Create a lollipop chart to show the count of annotations for different labels.

        Parameters:
        - df (pl.DataFrame): The dataframe containing the annotation data.
        """
        if len(df) == 0:
            return None

        # Group by label and count the number of annotations
        count_df = (
            df.group_by("label")
            .agg(pl.count("token").alias("count"))
            .filter(pl.col("label") != "")
            .sort("count", descending=True)
        )

        # Create the pie chart
        fig = px.pie(
            count_df,
            names="label",
            values="count",
            title="Count of Annotations per Label",
            labels={"label": "Annotation Label", "count": "Count"},
        )

        fig.update_traces(
            textinfo="percent+label",  # Display percentage and label on slices
        )

        fig.update_layout(autosize=True)

        return fig
    return plot_annotation_counts,


@app.cell
def __():
    import anywidget
    import traitlets
    import json


    class MultiTextAnnotationWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
            let data = model.get("data");
            const labels = model.get("labels");
            let currentTextIndex = 0;
            let bufferSize = model.get("buffer_size");

            model.on("change:data", () => {
                data = model.get("data");
                currentTextIndex = 0;
                updateTextDisplay();
            });

            model.on("change:buffer_size", () => {
                bufferSize = model.get("buffer_size");
                updateTextDisplay();
            });

            // Create a container for the legend
            let legendContainer = document.createElement("div");
            legendContainer.className = "legend-container";
            el.appendChild(legendContainer);

            // Create a container for the text
            let textContainer = document.createElement("div");
            textContainer.className = "text-container";
            el.appendChild(textContainer);

            let beforeBufferContainer = document.createElement("div");
            beforeBufferContainer.className = "buffer-container before-buffer";
            let mainTextContainer = document.createElement("div");
            mainTextContainer.className = "main-text-container";
            let afterBufferContainer = document.createElement("div");
            afterBufferContainer.className = "buffer-container after-buffer";

            textContainer.appendChild(beforeBufferContainer);
            textContainer.appendChild(mainTextContainer);
            textContainer.appendChild(afterBufferContainer);

            // Create navigation buttons
            let navContainer = document.createElement("div");
            navContainer.className = "nav-container";
            let prevButton = document.createElement("button");
            prevButton.innerText = "previous";
            prevButton.className = "nav-button";
            prevButton.addEventListener("click", () => navigateText(-1));
            let nextButton = document.createElement("button");
            nextButton.innerText = "next";
            nextButton.className = "nav-button";
            nextButton.addEventListener("click", () => navigateText(1));

            let pageIndicator = document.createElement("span");
            pageIndicator.className = "page-indicator";

            navContainer.appendChild(prevButton);
            navContainer.appendChild(pageIndicator);
            navContainer.appendChild(nextButton);
            el.appendChild(navContainer);

            // Create a container for the labels
            let labelContainer = document.createElement("div");
            labelContainer.className = "label-container";
            for (let [label, color] of Object.entries(labels)) {
                let labelButton = document.createElement("button");
                labelButton.innerText = label;
                labelButton.style.backgroundColor = color;
                labelButton.className = "label-button";
                labelButton.addEventListener("click", () => addAnnotation(label, color));
                labelContainer.appendChild(labelButton);
            }
            el.appendChild(labelContainer);

            // Create remove button and note textarea (initially hidden)
            let actionContainer = document.createElement("div");
            actionContainer.className = "action-container";
            actionContainer.style.display = "none";

            let removeButton = document.createElement("button");
            removeButton.innerText = "Remove";
            removeButton.className = "action-button";
            removeButton.addEventListener("click", removeAnnotation);

            let noteTextArea = document.createElement("textarea");
            noteTextArea.placeholder = "Add notes here...";
            noteTextArea.className = "note-textarea";
            noteTextArea.addEventListener("input", updateNote);

            actionContainer.appendChild(removeButton);
            actionContainer.appendChild(noteTextArea);
            el.appendChild(actionContainer);

            let currentAnnotation = null;

            function navigateText(direction) {
                currentTextIndex += direction;
                if (currentTextIndex < 0) currentTextIndex = data.length - 1;
                if (currentTextIndex >= data.length) currentTextIndex = 0;
                updateTextDisplay();
            }

            function updateTextDisplay() {
                let currentResult = JSON.parse(model.get("result"));
                let currentAnnotations = currentResult[currentTextIndex] || [];

                let bufferBefore = "";
                let bufferAfter = "";
                let mainText = data[currentTextIndex];

                if (bufferSize > 0) {
                    for (let i = 1; i <= bufferSize; i++) {
                        let beforeIndex = currentTextIndex - i;
                        let afterIndex = currentTextIndex + i;

                        if (beforeIndex >= 0) {
                            bufferBefore = data[beforeIndex] + "\\n" + bufferBefore;
                        }
                        if (afterIndex < data.length) {
                            bufferAfter += "\\n" + data[afterIndex];
                        }
                    }
                }

                // Apply annotations only to main text
                currentAnnotations.sort((a, b) => b.start - a.start);

                for (let annotation of currentAnnotations) {
                    let before = mainText.slice(0, annotation.start);
                    let annotated = mainText.slice(annotation.start, annotation.end);
                    let after = mainText.slice(annotation.end);
                    mainText = before + `<span class="annotation" style="background-color: ${labels[annotation.label]};" data-id="${annotation.id}" data-label="${annotation.label}">` + annotated + '</span>' + after;
                    }

                beforeBufferContainer.innerHTML = bufferBefore;
                mainTextContainer.innerHTML = mainText;
                afterBufferContainer.innerHTML = bufferAfter;

                pageIndicator.textContent = `Task ${currentTextIndex + 1} of ${data.length}`;
                updateLegend(currentAnnotations);
            }

            function updateLegend(annotations) {
                let legendHTML = '';
                for (let [label, color] of Object.entries(labels)) {
                    let annotationsForLabel = annotations.filter(a => a.label === label);
                    let annotatedTexts = annotationsForLabel.map(a => a.text).join(', ');
                    legendHTML += `
                        <div class="legend-row">
                            <div class="legend-label">
                                <span class="legend-color" style="background-color: ${color};"></span>
                                ${label}
                            </div>
                            <div class="legend-text">${annotatedTexts}</div>
                        </div>
                    `;
                }
                legendContainer.innerHTML = legendHTML;
            }

            function addAnnotation(label, color) {
                let selection = getSelectionWithinShadowRoot(textContainer);

                if (selection.rangeCount === 0) return;

                let range = selection.getRangeAt(0);

                let selectedText = range.toString();
                let startContainer = range.startContainer;
                let endContainer = range.endContainer;

                // Ensure the selection is within the main text container
                if (!mainTextContainer.contains(startContainer) || !mainTextContainer.contains(endContainer)) {
                    alert("Please select text only within the main text area.");
                    return;
                }

                let mainTextContent = mainTextContainer.textContent;
                let startOffset = getTextOffset(mainTextContainer, range.startContainer, range.startOffset);
                let endOffset = getTextOffset(mainTextContainer, range.endContainer, range.endOffset);

                let annotationId = `${currentTextIndex}-${Date.now()}`;

                let currentResult = JSON.parse(model.get("result"));
                if (!currentResult[currentTextIndex]) {
                    currentResult[currentTextIndex] = [];
                }
                currentResult[currentTextIndex].push({
                    id: annotationId,
                    text: selectedText,
                    label: label,
                    start: startOffset,
                    end: endOffset,
                    note: ""  // Initialize with an empty note
                });
                model.set("result", JSON.stringify(currentResult));
                model.save_changes();

                updateTextDisplay();
                noteTextArea.value = "";  // Clear the text area after adding annotation
            }

            function getTextOffset(root, node, offset) {
                let walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
                let currentOffset = 0;

                while (walker.nextNode()) {
                    if (walker.currentNode === node) {
                        return currentOffset + offset;
                    }
                    currentOffset += walker.currentNode.length;
                }

                return -1;
            }

            function getSelectionWithinShadowRoot(container) {
                if (container.getRootNode() instanceof ShadowRoot) {
                    return container.getRootNode().getSelection();
                }
                return window.getSelection();
            }

            function getTextPosition(node, offset) {
                let position = 0;
                let walker = document.createTreeWalker(textContainer, NodeFilter.SHOW_TEXT, null, false);

                while (walker.nextNode()) {
                    if (walker.currentNode === node) {
                        return position + offset;
                    }
                    position += walker.currentNode.length;
                }

                return position;
            }

            function removeAnnotation() {
                if (currentAnnotation) {
                    let currentResult = JSON.parse(model.get("result"));
                    let textAnnotations = currentResult[currentTextIndex];
                    let index = textAnnotations.findIndex(item => item.id === currentAnnotation.id);
                    if (index > -1) {
                        textAnnotations.splice(index, 1);
                        model.set("result", JSON.stringify(currentResult));
                        model.save_changes();
                    }

                    currentAnnotation = null;
                    actionContainer.style.display = "none";

                    updateTextDisplay();
                }
            }

            function updateNote() {
                if (currentAnnotation) {
                    let currentResult = JSON.parse(model.get("result"));
                    let textAnnotations = currentResult[currentTextIndex];
                    let annotation = textAnnotations.find(item => item.id === currentAnnotation.id);
                    if (annotation) {
                        annotation.note = noteTextArea.value;
                        model.set("result", JSON.stringify(currentResult));
                        model.save_changes();
                    }
                }
            }

            textContainer.addEventListener("mouseup", (event) => {
                let target = event.target;
                if (target.classList.contains("annotation")) {
                    let currentResult = JSON.parse(model.get("result"));
                    let annotation = currentResult[currentTextIndex].find(a => a.id === target.dataset.id);
                    currentAnnotation = {
                        id: target.dataset.id,
                        label: target.dataset.label
                    };
                    actionContainer.style.display = "flex";
                    noteTextArea.value = annotation.note || "";  // Populate textarea with the existing note
                } else {
                    currentAnnotation = null;
                    actionContainer.style.display = "none";
                }
            });

            updateTextDisplay();
        }
        export default { render };
        """
        _css = """
        .text-container {
            border: 1px solid #444;
            padding: 15px;
            margin-bottom: 10px;
            font-family: Arial, sans-serif;
            font-size: 13px;
            line-height: 1.5;
            border-radius: 10px;
            white-space: pre-wrap;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .buffer-container {
            padding: 15px;
            font-weight: 200;
            opacity: 0.6;
            font-style: italic;
            border-radius: 8px;
            margin: 0, 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .before-buffer {
            border-left: 4px solid #3498db;
        }

        .main-text-container {
            padding: 20px;
            font-weight: 600;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #2ecc71;
        }

        .after-buffer {
            border-left: 4px solid #e74c3c;
        }

        .legend-container {
            display: grid;
            grid-template-columns: 1fr 1fr; /* Two columns for the legend */
            gap: 10px;
            margin-top: 10px;
            padding: 12px;
            border-radius: 8px;
            font-size: 12px;
        }

        .legend-row {
            display: flex;
            align-items: center;
        }

        .legend-label {
            display: flex;
            align-items: center;
            margin-right: 10px;
            width: 144px;
        }

        .legend-color {
            display: inline-block;
            width: 8px;
            height: 8px;
            margin-right: 5px;
            border-radius: 50%;
        }

        .legend-text {
            font-size: 11px;
        }

        .label-container, .action-container {
            margin-bottom: 10px;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            width: 500px;
            margin-left: auto;
            margin-right: auto;
        }

        .nav-container {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            margin: 15px 0;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 10px;
        }

        .nav-button, .label-button, .action-button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 0.6em 1em;
            margin: 0.3em;
            cursor: pointer;
            border-radius: 5px;
            font-size: 12px;
            transition: background-color 0.3s;
        }

        .nav-button:hover, .label-button:hover, .action-button:hover {
            background-color: #0056b3;
        }

        .annotation {
            cursor: pointer;
            transition: opacity 0.3s;
        }

        .annotation:hover {
            opacity: 0.7;
        }

        .note-textarea {
            width: 250px;
            height: 60px;
            margin-left: 10px;
            padding: 5px;
            font-size: 14px;
            border-radius: 5px;
            resize: vertical;
            border: 1px solid #ccc;
        }

        .page-indicator {
            font-size: 11px;
        }
        """
        data = traitlets.List().tag(sync=True)
        labels = traitlets.Dict().tag(sync=True)
        result = traitlets.Unicode().tag(sync=True)
        buffer_size = traitlets.Int(default_value=0).tag(sync=True)

        def __init__(self, data, labels, buffer_size=0):
            super().__init__()
            self.data = data
            self.labels = labels
            self.result = json.dumps({i: [] for i in range(len(data))})
            self.buffer_size = buffer_size

        @traitlets.observe("data")
        def _update_result(self, change):
            self.result = json.dumps({i: [] for i in range(len(self.data))})

        @traitlets.observe("buffer_size")
        def _update_buffer_size(self, change):
            pass
    return MultiTextAnnotationWidget, anywidget, json, traitlets


@app.cell(hide_code=True)
def __(OpenAI, assist_form):
    if assist_form.value is not None and assist_form.value["api_key"] is not None:
        client = OpenAI(api_key=assist_form.value["api_key"])
    else:
        client = OpenAI()
    return client,


@app.cell(hide_code=True)
def __():
    from pydantic import BaseModel, Field
    return BaseModel, Field


@app.cell(hide_code=True)
def __(BaseModel, Field):
    class TokenLabel(BaseModel):
        token: str = Field(description="")
        label: str
        start: int
        stop: int
        confidence: float = Field(description="Confidence in the label (0-1)")


    class AnnotationResponse(BaseModel):
        answer: list[TokenLabel]
    return AnnotationResponse, TokenLabel


@app.cell(hide_code=True)
def __(AnnotationResponse, system_prompt):
    def get_annotation_response_pydantic(query: str, client):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt.value},
                {"role": "user", "content": query},
            ],
            response_format=AnnotationResponse,
        )

        return completion.choices[0].message.parsed
    return get_annotation_response_pydantic,


@app.cell(hide_code=True)
def __(AnnotationResponse, pl):
    def response_to_dataframe(token_labels: AnnotationResponse) -> pl.DataFrame:
        # Extract data from the list of TokenLabel objects
        data = {
            "token": [label.token for label in token_labels],
            "label": [label.label for label in token_labels],
            "start": [label.start for label in token_labels],
            "stop": [label.stop for label in token_labels],
            "confidence": [label.confidence for label in token_labels],
        }

        return pl.DataFrame(data)
    return response_to_dataframe,


@app.cell(hide_code=True)
def __(
    assist_form,
    client,
    get_annotation_response_pydantic,
    mo,
    response_to_dataframe,
):
    mo.stop(assist_form.value is None)

    response_pydantic = get_annotation_response_pydantic(
        query=assist_form.value["user_query"], client=client
    )
    response_df = response_to_dataframe(response_pydantic.answer)
    return response_df, response_pydantic


@app.cell(hide_code=True)
def __():
    import plotly.express as px


    def generate_label2color(labels):
        """
        Generate a label2color dictionary with aesthetic and color-blind friendly colors.

        Args:
        labels (list of str): A sequence of string labels to assign colors.

        Returns:
        dict: A dictionary where keys are labels and values are corresponding color codes.
        """
        # Define a color scale from Plotly, which is color-blind friendly
        color_scale = px.colors.qualitative.Plotly

        # Determine the number of colors needed
        num_colors = len(labels)

        # Cycle through colors if the number of labels exceeds the color scale length
        sampled_colors = [
            color_scale[i % len(color_scale)] for i in range(num_colors)
        ]

        # Generate the label2color dictionary
        label2color = {
            label: color for label, color in zip(labels, sampled_colors)
        }

        return label2color
    return generate_label2color, px


@app.cell(hide_code=True)
def __():
    import marimo as mo
    return mo,


@app.cell(hide_code=True)
def __():
    text = """Patient admitted to ward at 19:45. Medication administration scheduled for 20:00. Stalevo and Neodopastone were set up in the treatment room. At 20:10, empty packages of Stalevo and Neodopastone were observed in the drug case, but Lunesta package was missing. Patient reported setting Lunesta aside for later consumption. Thorough search of bedside area yielded no results.

    At 20:31, nurse reported potential accidental ingestion of medication package by patient. Patient complained of chest discomfort. On-duty physician was immediately notified. Emergency CT scan was ordered and performed, revealing a foreign body in the upper esophagus. Dr. Smith conducted an emergency endoscopy, successfully removing a PTP sheet from the upper esophagus. Minor bleeding was observed during the procedure, but patient's discomfort subsided post-intervention.

    Post-procedure instructions included NPO (nil per os) status for the remainder of the evening. Diet to be reassessed the following day. Patient had self-administered Levemir via subcutaneous injection. Verbal instructions were given to reduce dosage from 8 units to 4 units, but actual dose reduction was not implemented.

    21:15: Vital signs monitored. BP 130/80 mmHg, HR 72 bpm, RR 16/min, SpO2 98% on room air. Patient alert and oriented x3.

    22:00: Patient reported mild soreness in throat. Advised to rest voice and maintain NPO status. Ice chips provided for comfort.

    23:00: Night shift nurse reported Lunesta still missing from medication case. Thorough room search conducted but unsuccessful.

    00:30: Patient sleeping comfortably. No signs of respiratory distress or increased discomfort.

    03:00: Routine vitals check. BP 125/75 mmHg, HR 68 bpm, RR 14/min, SpO2 99% on room air.

    06:00: Patient awoke, reporting improved comfort. Mild throat irritation persists but significantly reduced.

    07:00: Morning rounds conducted. Dr. Johnson reviewed CT scan results, confirming no additional complications. Endoscopy report indicated successful removal of foreign body with minimal trauma to esophageal lining.

    08:00: Dietary consult ordered to assess appropriate diet progression.

    09:30: Patient able to swallow small sips of water without difficulty. Soft diet to be introduced gradually.

    10:15: Pharmacist consulted regarding medication protocols. Discussed importance of proper medication storage and administration with nursing staff.

    11:00: Patient educated on medication safety, emphasizing importance of not consuming medications in their packaging.

    12:00: Lunch served - clear liquids tolerated well.

    14:00: Follow-up CT scan scheduled for tomorrow to ensure complete resolution.

    16:00: Patient ambulating in hallway with assistance, reporting no dizziness or discomfort.

    18:00: Evening medication round. All medications accounted for and administered as prescribed, including adjusted Levemir dose.

    19:30: Patient comfortable, watching TV. No complaints of pain or discomfort.

    20:00: Night nurse briefed on patient's condition and medication protocol for overnight monitoring.

    Citations:
    [1] https://direct.mit.edu/dint/article/3/3/402/102637/Medical-Named-Entity-Recognition-from-Un-labelled
    [2] https://github.com/iajaykarthick/NER-medical-text
    [3] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10651400/
    [4] https://academic.oup.com/jamia/article/31/9/1812/7590607
    [5] https://www.sciencedirect.com/science/article/pii/S1386505623001405
    [6] https://www.kiwihealth.com/blog/mastering-clinical-note-writing-tips
    [7] https://blog.dentrixascend.com/2022/06/01/save-time-with-clinical-note-templates/"""
    return text,


@app.cell(hide_code=True)
def __(mo):
    system_prompt = mo.ui.text_area(
        """You are a clinical named entity recognition expert. Your task is to analyze medical sentences and annotate words that represent specific named entities. For each sentence provided, identify and label words or phrases that correspond to the following entity types:

    1. Strength_rate: The rate of strength of a drug or compound.
    2. Drug: Any medicinal or chemical substance being used.
    3. Route: The method or path of drug administration (e.g., oral, IV).
    4. Duration: The length of time a treatment or drug administration lasts.
    5. Frequency: How often a drug is administered (e.g., once daily, twice weekly).
    6. Dosage: The amount of a drug or substance to be taken.
    7. Form_form: The form of the drug (e.g., tablet, injection).
    8. Date: Any relevant date associated with drug administration or treatment.
    9. Strength_amount: The quantity or amount of the drug's strength (e.g., 500 mg).
    10. Strength_concentration: The concentration level of the drug's strength (e.g., 10%).
    11. Time: The time of day or a specific time related to drug administration.

    If a label is "O", skip it.

    Annotate each word in the given sentence that corresponds to one of these entity types. If a word does not correspond to any of the listed entity types, leave it unannotated. Ensure that your annotations are accurate and comprehensive, capturing all relevant named entities in the sentence.
    """,
        label="System Prompt",
        rows=20,
        full_width=True,
        disabled=True,
    )
    system_prompt
    return system_prompt,


if __name__ == "__main__":
    app.run()
