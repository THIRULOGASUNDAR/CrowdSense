importScripts("https://www.gstatic.com/firebasejs/9.22.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/9.22.1/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyCQeziXEWW0bjqTlyASauTV0H4Q1PjPeQc",
  authDomain: "csauth-967ed.firebaseapp.com",
  projectId: "csauth-967ed",
  storageBucket: "csauth-967ed.firebasestorage.app",
  messagingSenderId: "267260771528",
  appId: "1:267260771528:web:99a386d1b725586eb6b9fd",
  measurementId: "G-V7X3X6E56E"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log('Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/icons/Icon-192.png'
  };

  return self.registration.showNotification(notificationTitle, notificationOptions);
});
