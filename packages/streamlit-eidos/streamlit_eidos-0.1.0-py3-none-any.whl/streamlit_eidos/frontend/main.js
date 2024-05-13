/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */

let eidosEventList = [];

function onRender(event) {
  // Only run the render code the first time the component is loaded.
  const container = document.getElementById("eidos-container");
  const {
    key,
    spec,
    patch,
    height,
    events = [],
    renderer = "https://render.eidos.oceanum.io",
  } = event.detail.args;

  if (!window.eidos) {
    window.eidos = {};
  }

  const updateSpec = () => {
    const messageTarget = document.getElementById(key).contentWindow;
    if (spec) {
      messageTarget.postMessage({ id: key, type: "spec", payload: spec }, "*");
    } else if (patch) {
      messageTarget.postMessage(
        { id: key, type: "patch", payload: patch },
        "*"
      );
    }
  };

  const eidosEventHandler = (event) => {
    console.log("eidosEventHandler", event);
    const { action, source, data, coordinate } = event.data;
    if (events.includes(action)) {
      Streamlit.setComponentValue({ action, data, source, coordinate });
    } else if (action == "status" && data.status == "ready") {
      updateSpec();
    }
  };

  if (!window.eidos[key]) {
    let iframe = document.createElement("iframe");
    iframe.src = `${renderer}?id=${key}`;
    iframe.width = "100%";
    iframe.height = height;
    iframe.classList.add("eidos-iframe");
    container.appendChild(iframe);
    iframe.key = key;
    iframe.id = key;
    window.eidos[key] = true;
    window.addEventListener("message", eidosEventHandler);
  } else {
    updateSpec(spec, patch);
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady();
// Render with the correct height, if this is a fixed-height component
