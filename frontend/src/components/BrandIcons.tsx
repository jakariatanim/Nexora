import React from 'react';

// Authentic Official WhatsApp Icon (Green Circular Badge with White Bubble & Phone)
export const WhatsAppIcon: React.FC<{ className?: string }> = ({ className = "w-6 h-6" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="12" fill="#25D366"/>
    <path d="M12.012 5.5C8.423 5.5 5.5 8.423 5.5 12.012c0 1.218.337 2.36.923 3.336L5.5 18.5l3.242-.898a6.47 6.47 0 003.27.876c3.588 0 6.512-2.923 6.512-6.512 0-3.589-2.924-6.466-6.512-6.466zm3.805 9.213c-.159.447-.923.855-1.289.909-.333.048-.755.068-1.221-.081-.282-.09-.643-.209-1.107-.408-1.95-.836-3.219-2.822-3.316-2.951-.097-.13-.794-1.057-.794-2.016 0-.959.502-1.43.68-1.625.178-.195.39-.244.52-.244.13 0 .261.002.375.008.12.006.28-.046.438.333.16.388.544 1.332.593 1.43.049.098.081.213.016.342-.065.13-.098.212-.195.326-.098.114-.206.255-.294.342-.098.098-.2.204-.086.4.114.195.508.838 1.09 1.356.75.668 1.383.875 1.578.972.195.097.31.081.424-.049.114-.13.488-.569.619-.764.13-.195.26-.163.439-.098.179.065 1.139.537 1.334.635.195.098.326.146.374.228.049.081.049.472-.11 0.919z" fill="#FFFFFF"/>
  </svg>
);

// Authentic Official Facebook Icon (Facebook Brand Blue Badge with White 'f')
export const FacebookIcon: React.FC<{ className?: string }> = ({ className = "w-6 h-6" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="12" fill="#1877F2"/>
    <path d="M15.117 12.834l.43-2.8h-2.69V8.217c0-.768.375-1.517 1.583-1.517h1.225V4.316c-.27-.036-1.198-.116-2.278-.116-2.324 0-3.844 1.409-3.844 3.96v2.074H7.098v2.8h2.444v6.772c.49.077.99.118 1.5.118s1.01-.041 1.5-.118v-6.772h2.575z" fill="#FFFFFF"/>
  </svg>
);

// Authentic Official LinkedIn Icon (Brand Blue Circular Badge with White 'in')
export const LinkedInIcon: React.FC<{ className?: string }> = ({ className = "w-6 h-6" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="12" fill="#0A66C2"/>
    <path d="M7.8 9.6H5.4V17.4H7.8V9.6ZM6.6 5.6C5.8 5.6 5.2 6.2 5.2 7C5.2 7.8 5.8 8.4 6.6 8.4C7.4 8.4 8 7.8 8 7C8 6.2 7.4 5.6 6.6 5.6ZM18.6 12.2C18.6 10.4 17.2 9.4 15.6 9.4C14.4 9.4 13.6 10.1 13.2 10.7V9.6H11V17.4H13.4V13.5C13.4 12.5 13.6 11.5 14.9 11.5C16.1 11.5 16.2 12.6 16.2 13.6V17.4H18.6V12.2Z" fill="#FFFFFF"/>
  </svg>
);

// Authentic Official Email Icon (Red Circular Badge with White Envelope)
export const EmailIcon: React.FC<{ className?: string }> = ({ className = "w-6 h-6" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="12" fill="#EA4335"/>
    <path d="M5.5 8C5.5 7.17 6.17 6.5 7 6.5H17C17.83 6.5 18.5 7.17 18.5 8V16C18.5 16.83 17.83 17.5 17 17.5H7C6.17 17.5 5.5 16.83 5.5 16V8ZM7 8L12 11.5L17 8H7ZM17 9.8L12 13.3L7 9.8V16H17V9.8Z" fill="#FFFFFF"/>
  </svg>
);
