const enableBrowserNotifications = () => {
if (!("Notification" in window)) {
return;
}

if (Notification.permission === "default") {
    Notification.requestPermission();
}

};

const showBrowserNotification = (title, message) => {
if (!("Notification" in window)) {
return;
}

if (Notification.permission === "granted") {
    new Notification(title, {
        body: message,
        icon: "/static/images/logo.png"
    });
}

};

document.addEventListener("DOMContentLoaded", () => {
enableBrowserNotifications();

const notificationData = document.getElementById("notification-data");

if (notificationData) {
    const title = notificationData.dataset.title;
    const message = notificationData.dataset.message;

    if (title && message) {
        showBrowserNotification(title, message);
    }
}

});