<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hydro Vision Flood Alerts</title>

<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #071525;
    color: white;
    text-align: center;
}
.container {
    max-width: 500px;
    margin: 35px auto;
    padding: 25px;
    background: #12263d;
    border-radius: 18px;
}
h1 { color: #36e0cf; }
p { line-height: 1.6; color: #d2deec; }
button {
    width: 100%;
    padding: 14px;
    margin: 10px 0;
    border: none;
    border-radius: 8px;
    background: #36e0cf;
    color: #071525;
    font-weight: bold;
    cursor: pointer;
}
input {
    width: 90%;
    padding: 10px;
    margin: 6px;
    border-radius: 6px;
}
#status {
    margin-top: 15px;
    padding: 12px;
    background: #071525;
    border-radius: 8px;
    overflow-wrap: anywhere;
}
</style>
</head>

<body>
<div class="container">
    <h1>🌧️ HYDRO VISION</h1>
    <h3>Flood Notification System</h3>

    <p>
        Location-Based Flood Risk Alerts<br>
        Notification Radius: 1 KM
    </p>

    <button onclick="enableNotifications()">
        Enable Location & Notifications
    </button>

    <hr>

    <h3>Simulate Flood Alert</h3>

    <input id="floodLat" type="number"
           step="any" value="17.3850"
           placeholder="Flood latitude">

    <input id="floodLon" type="number"
           step="any" value="78.4867"
           placeholder="Flood longitude">

    <button onclick="sendDemoAlert()">
        🚨 Trigger Demo Flood Alert
    </button>

    <div id="status">Waiting for permission...</div>
</div>

<script>
let userLat = null;
let userLon = null;

// Calculate distance between two coordinates in kilometres
function haversine(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const rad = d => d * Math.PI / 180;

    const dLat = rad(lat2 - lat1);
    const dLon = rad(lon2 - lon1);

    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(rad(lat1)) *
        Math.cos(rad(lat2)) *
        Math.sin(dLon / 2) ** 2;

    return 2 * R * Math.atan2(
        Math.sqrt(a), Math.sqrt(1 - a)
    );
}

// Request location and notification permission
async function enableNotifications() {
    const status = document.getElementById("status");

    try {
        if (!navigator.geolocation) {
            throw new Error("Geolocation is not supported.");
        }

        if (!("Notification" in window)) {
            throw new Error("Notifications are not supported.");
        }

        const permission = await Notification.requestPermission();

        if (permission !== "granted") {
            throw new Error("Please allow notifications.");
        }

        status.textContent = "Getting your location...";

        navigator.geolocation.getCurrentPosition(
            position => {
                userLat = position.coords.latitude;
                userLon = position.coords.longitude;

                status.textContent =
                    "✅ Notifications enabled\n" +
                    "Latitude: " + userLat.toFixed(5) +
                    "\nLongitude: " + userLon.toFixed(5) +
                    "\nReady to test flood alerts.";

                // Register for location updates during this demo session
                navigator.geolocation.watchPosition(p => {
                    userLat = p.coords.latitude;
                    userLon = p.coords.longitude;
                }, () => {}, { enableHighAccuracy: true });
            },
            error => {
                status.textContent =
                    "Location unavailable: " + error.message;
            },
            { enableHighAccuracy: true, timeout: 15000 }
        );
    } catch (error) {
        status.textContent = error.message;
    }
}

// Trigger a simulated location-based alert
function sendDemoAlert() {
    const status = document.getElementById("status");

    if (userLat === null || userLon === null) {
        status.textContent =
            "Enable location first, then trigger the alert.";
        return;
    }

    const floodLat = Number(
        document.getElementById("floodLat").value
    );
    const floodLon = Number(
        document.getElementById("floodLon").value
    );

    if (!Number.isFinite(floodLat) ||
        !Number.isFinite(floodLon) ||
        floodLat < -90 || floodLat > 90 ||
        floodLon < -180 || floodLon > 180) {
        status.textContent = "Enter valid flood coordinates.";
        return;
    }

    const distance = haversine(
        userLat, userLon, floodLat, floodLon
    );

    if (distance <= 1) {
        const title = "🚨 Hydro Vision Flood Alert";
        const message =
            "High flood risk detected near your location. " +
            "Follow official local safety instructions.";

        status.textContent =
            "⚠️ HIGH FLOOD RISK\n" +
            "Distance: " + distance.toFixed(3) + " km\n" +
            "You are inside the 1 km alert radius.";

        if (Notification.permission === "granted") {
            new Notification(title, { body: message });
        }
    } else {
        status.textContent =
            "You are outside the alert radius.\n" +
            "Distance from risk point: " +
            distance.toFixed(2) + " km\n" +
            "No nearby alert generated.";
    }
}
</script>
</body>
</html>