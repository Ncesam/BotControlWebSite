/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx,css}", // Добавь CSS
    ],
    theme: {
        extend: {
            colors: {
                baseColor: "#001f54"
            }
            
        }
    },
    plugins: [],
};
