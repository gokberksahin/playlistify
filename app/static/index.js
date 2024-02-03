let spotifyEmbedApi = null;
let embedController = null

window.onSpotifyIframeApiReady = (IFrameAPI) => {
    console.log("iframe ready");
    spotifyEmbedApi = IFrameAPI;
};

document
    .getElementById("sentence-form")
    .addEventListener("submit", function (e) {
        if (e.target.method == "get") return;
        e.preventDefault(); // This will prevent the default form submission
        const formData = new FormData(this);
        fetch("/playlist", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (embedController !== null) {
                    console.log('loading uri');
                    embedController.loadUri(data.uri);
                    return;
                }
                const embedElement = document.getElementById("embed-iframe");
                const callback = (controller) => {
                    embedController = controller
                }
                spotifyEmbedApi.createController(embedElement, { uri: data.uri }, callback);
            })
            .catch((error) => console.error("Error:", error));
    });