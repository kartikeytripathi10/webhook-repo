function formatEvent(event) {
    const date = new Date(event.timestamp).toUTCString();
    if (event.type === "PUSH") {
        return `${event.author} pushed to ${event.to_branch} on ${date}`;
    } else if (event.type === "PULL_REQUEST") {
        return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${date}`;
    } else if (event.type === "MERGE") {
        return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${date}`;
    }
}

async function fetchEvents() {
    const res = await fetch('/events');
    const events = await res.json();
    const container = document.getElementById("events");
    container.innerHTML = events.map(formatEvent).join('<br><br>');
}

setInterval(fetchEvents, 15000);
fetchEvents();
