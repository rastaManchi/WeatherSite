document.addEventListener('DOMContentLoaded', function () {
    // Current date
    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    // Weather conditions
    const weatherConditions = [
        {
            type: 'sunny',
            icon: '☀️',
            minTemp: 20,
            maxTemp: 35,
            morning_bg: '/media/GIFs/clear/morning_clear.gif',
            day_bg: '/media/GIFs/clear/day_clear.gif',
            evening_bg: '/media/GIFs/clear/evening_clear.gif',
            night_bg: "/media/GIFs/clear/night_clear.gif"
        },
        {
            type: 'rain',
            icon: '🌧️',
            minTemp: 20,
            maxTemp: 35,
            morning_bg: '/media/GIFs/rainy/morning_rainy.gif',
            day_bg: '/media/GIFs/rainy/day_rain.gif',
            evening_bg: '/media/GIFs/rainy/evening_rain.gif',
            night_bg: "/media/GIFs/rainy/night_rain.dif"
        }
    ];

    // DOM elements
    const calendarGrid = document.getElementById('calendarGrid');
    const currentMonthElement = document.getElementById('currentMonth');
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');
    const outfitModal = document.getElementById('outfitModal');
    const closeModalBtn = document.getElementById('closeModal');
    const modalDate = document.getElementById('modalDate');
    const modalWeatherIcon = document.getElementById('modalWeatherIcon');
    const modalWeatherDesc = document.getElementById('modalWeatherDesc');
    const modalTemp = document.getElementById('modalTemp');
    const outfitRecommendation = document.getElementById('outfitRecommendation');
    const weatherBackground = document.getElementById('weatherBackground');

    // Event listeners
    prevMonthBtn.addEventListener('click', () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar();
    });

    nextMonthBtn.addEventListener('click', () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar();
    });

    closeModalBtn.addEventListener('click', () => {
        outfitModal.classList.add('hidden');
    });

    outfitModal.addEventListener('click', (e) => {
        if (e.target === outfitModal) {
            outfitModal.classList.add('hidden');
        }
    });

    // Generate random weather for a day
    function getRandomWeather() {
        const randomIndex = Math.floor(Math.random() * weatherConditions.length);
        return weatherConditions[randomIndex];
    }

    // Render calendar
    function renderCalendar() {
        // Update month display
        const monthNames = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"];
        currentMonthElement.textContent = `${monthNames[currentMonth]} ${currentYear}`;

        // Clear previous calendar
        calendarGrid.innerHTML = '';

        // Get first day of month and total days
        const firstDay = new Date(currentYear, currentMonth, 1).getDay();
        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

        // Add empty cells for days before first day
        for (let i = 0; i < firstDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'h-24 bg-gray-800 rounded-lg opacity-50';
            calendarGrid.appendChild(emptyCell);
        }

        // Add day cells
        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'day-cell bg-gray-800 rounded-lg p-2 h-24 flex flex-col cursor-pointer hover:bg-gray-700 transition';

            // Random weather for the day
            const weather = getRandomWeather();
            const temp = Math.floor(Math.random() * (weather.maxTemp - weather.minTemp + 1)) + weather.minTemp;

            // Date for this cell
            const cellDate = new Date(currentYear, currentMonth, day);

            // If it's today, highlight it
            if (day === currentDate.getDate() && currentMonth === currentDate.getMonth() && currentYear === currentDate.getFullYear()) {
                dayCell.classList.add('border-2', 'border-blue-400');
                updateBackground(weather);
            }

            // Day number
            const dayNumber = document.createElement('div');
            dayNumber.className = 'text-right font-medium';
            dayNumber.textContent = day;
            dayCell.appendChild(dayNumber);

            // Weather icon
            const weatherIcon = document.createElement('div');
            weatherIcon.className = 'weather-icon text-2xl text-center my-1';
            weatherIcon.textContent = weather.icon;
            dayCell.appendChild(weatherIcon);

            // Temperature
            const tempElement = document.createElement('div');
            tempElement.className = 'text-center text-sm';
            tempElement.textContent = `${temp}°C`;
            dayCell.appendChild(tempElement);

            // Store weather data on the cell
            dayCell.dataset.date = cellDate.toDateString();
            dayCell.dataset.weatherType = weather.type;
            dayCell.dataset.weatherIcon = weather.icon;
            dayCell.dataset.temperature = temp;

            // Click event for outfit recommendation
            dayCell.addEventListener('click', () => {
                openOutfitModal(day, weather, temp, cellDate);
            });

            calendarGrid.appendChild(dayCell);
        }

        // Update background based on current weather
    }

    // Open outfit recommendation modal
    function openOutfitModal(day, weather, temp, date) {
        const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        modalDate.textContent = date.toLocaleDateString('en-US', dateOptions);
        modalWeatherIcon.textContent = weather.icon;
        modalWeatherDesc.textContent = weather.type.charAt(0).toUpperCase() + weather.type.slice(1);
        modalTemp.textContent = `${temp}°C`;
        outfitRecommendation.textContent = "реком";
        outfitModal.classList.remove('hidden');
    }

    // Update background based on time of day and weather
    function updateBackground(weather) {
        const now = new Date();
        const hours = now.getHours();

        // Night time (8pm to 6am)
        if (hours >= 20 || hours < 6) {
            weatherBackground.style.backgroundImage = `url(${weather.night_bg})`;
        }
        // Morning (6am to 12pm)
        else if (hours >= 6 && hours < 12) {
            weatherBackground.style.backgroundImage = `url(${weather.morning_bg})`;
        }
        // Afternoon (12pm to 5pm)
        else if (hours >= 12 && hours < 17) {
            weatherBackground.style.backgroundImage = `url(${weather.day_bg})`;
        }
        // Evening (5pm to 8pm)
        else {
            weatherBackground.style.backgroundImage = `url(${weather.evening_bg})`;
        }
    }

    // Initialize
    renderCalendar();

    // Update background every hour
    setInterval(updateBackground, 3600000);
});