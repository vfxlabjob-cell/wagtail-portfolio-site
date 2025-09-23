document.addEventListener('DOMContentLoaded', function() {
    gsap.registerPlugin(ScrollTrigger);

    // ========================================================================
    // --- ШАГ 1: ВОССТАНОВЛЕНИЕ ПОЗИЦИИ СКРОЛЛА ---
    // ========================================================================
    const scrollPosition = sessionStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition, 10));
        sessionStorage.removeItem('scrollPosition');
    }

    // ========================================================================
    // --- ШАГ 2: СОХРАНЕНИЕ ПОЗИЦИИ ПЕРЕД КЛИКОМ ---
    // ========================================================================
    const filterControls = document.querySelector('.filter-controls');
    const filterContainer = document.querySelector('.filter-container');
    if (filterControls) {
        filterControls.addEventListener('click', function(e) {
            if (e.target.classList.contains('filter-btn')) {
                sessionStorage.setItem('scrollPosition', window.scrollY);
            }
        });
    }

    // Включаем стеклянный эффект при прокрутке вниз
    if (filterContainer) {
        const grid = document.querySelector('.portfolio-grid-full-width');
        const toggleGlass = () => {
            // Включаем стекло, когда верх фильтра пересекается с областью сетки
            const overGrid = grid ? (window.scrollY + filterContainer.offsetHeight) > (grid.offsetTop - 1) : (window.scrollY > 10);
            if (overGrid) filterContainer.classList.add('is-glass');
            else filterContainer.classList.remove('is-glass');
        };
        toggleGlass();
        window.addEventListener('scroll', toggleGlass, { passive: true });
    }

    // ========================================================================
    // --- КОД АНИМАЦИИ ---
    // ========================================================================
    const animSettings = {
        duration: 0.9,
        staggerAmount: 0.06,
        easeType: "power4.out",
        staggerFrom: "center"
    };

    const cards = gsap.utils.toArray('.portfolio-card');
    const images = gsap.utils.toArray('.card-image');

    gsap.set(cards, { autoAlpha: 0 });
    gsap.set(images, { scale: 0.8 });

    ScrollTrigger.matchMedia({
        "(min-width: 1025px)": function() {
            setupRowAnimations(9);
        },
        "(min-width: 768px) and (max-width: 1024px)": function() {
            setupRowAnimations(4);
        },
        "(max-width: 767px)": function() {
            setupRowAnimations(2);
        }
    });

    function setupRowAnimations(numColumns) {
        for (let i = 0; i < cards.length; i += numColumns) {
            const rowCards = cards.slice(i, i + numColumns);
            const rowImages = rowCards.map(card => card.querySelector('.card-image'));

            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: rowCards[0],
                    start: "top 85%",
                    
                    // === ГЛАВНОЕ ИЗМЕНЕНИЕ ЗДЕСЬ ===
                    // Этот параметр заставляет анимацию сработать только один раз.
                    // После этого ScrollTrigger для этого ряда отключается.
                    once: true,
                }
            });

            const staggerConfig = {
                each: animSettings.staggerAmount,
                grid: "auto",
                from: animSettings.staggerFrom
            };

            tl.to(rowCards, {
                autoAlpha: 1,
                duration: animSettings.duration,
                ease: animSettings.easeType,
                stagger: staggerConfig
            }, 0);

            tl.to(rowImages, {
                scale: 1,
                duration: animSettings.duration,
                ease: animSettings.easeType,
                force3D: true,
                rotation: 0.01,
                stagger: staggerConfig
            }, 0);
        }
    }

    // === Модальное видео: открытие по кнопке Play ===
    const modal = document.getElementById('videoModal');
    const modalPlayer = document.getElementById('videoModalPlayer');
    const modalClose = document.getElementById('videoModalClose');
    let lastFocusedButton = null;

    const openModalWithUrl = (url) => {
        if (!modal || !modalPlayer || !url) return;
        document.body.style.overflow = 'hidden';
        modal.setAttribute('aria-hidden', 'false');
        modal.classList.add('is-open');
        modalPlayer.src = url;
        modalPlayer.muted = false;
        try {
            const p = modalPlayer.play();
            if (p && typeof p.then === 'function') p.catch(() => {});
        } catch (_) {}
    };

    const closeModal = () => {
        if (!modal || !modalPlayer) return;
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        try { modalPlayer.pause(); } catch (_) {}
        modalPlayer.removeAttribute('src');
        try { modalPlayer.load(); } catch (_) {}
        document.body.style.overflow = '';
        if (lastFocusedButton) {
            try { lastFocusedButton.focus(); } catch (_) {}
            lastFocusedButton = null;
        }
    };

    // Клик по кнопке Play в карточке
    document.addEventListener('click', (e) => {
        const playBtn = e.target.closest('.overlay-btn.js-play');
        if (playBtn) {
            e.preventDefault();
            e.stopPropagation();
            const url = playBtn.getAttribute('data-video-url');
            lastFocusedButton = playBtn;
            if (url) openModalWithUrl(url);
        }
    });

    // Закрытие модалки
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target.hasAttribute('data-close-modal') || e.target === modal) closeModal();
        });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });
    }

    // === Тач-поведение карточек: первый тап показывает оверлей ===
    const isTouchCapable = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
    if (isTouchCapable) {
        document.addEventListener('click', (e) => {
            const cardLink = e.target.closest('.portfolio-card');
            if (!cardLink) return;

            const overlayVisible = cardLink.classList.contains('touch-active');
            const isPlay = e.target.closest('.overlay-btn.js-play');
            const isAnyButton = e.target.closest('.overlay-btn');

            // Если оверлей не виден и кликнули по карточке не по кнопке — показать и остановить переход
            if (!overlayVisible && !isAnyButton) {
                e.preventDefault();
                e.stopPropagation();
                // Скрыть у других
                document.querySelectorAll('.portfolio-card.touch-active').forEach(el => el.classList.remove('touch-active'));
                cardLink.classList.add('touch-active');
                return;
            }

            // Если оверлей виден и клик не по кнопке — просто спрятать
            if (overlayVisible && !isAnyButton) {
                e.preventDefault();
                cardLink.classList.remove('touch-active');
                return;
            }

            // Если кнопка Play — модалка обработается выше (и мы снимем touch-active)
            if (isPlay) {
                cardLink.classList.remove('touch-active');
                return;
            }
        }, { passive: false });

        // Скрывать оверлей при скролле
        let lastY = window.scrollY;
        window.addEventListener('scroll', () => {
            if (Math.abs(window.scrollY - lastY) > 2) {
                document.querySelectorAll('.portfolio-card.touch-active').forEach(el => el.classList.remove('touch-active'));
                lastY = window.scrollY;
            }
        }, { passive: true });

        // При открытии модалки — тоже снять
        document.addEventListener('click', (e) => {
            if (e.target.closest('.overlay-btn.js-play')) {
                document.querySelectorAll('.portfolio-card.touch-active').forEach(el => el.classList.remove('touch-active'));
            }
        });
    }

    // ========================================================================
    // --- КОНТАКТНЫЙ ВИДЖЕТ ---
    // ========================================================================
    const contactWidget = document.getElementById('contactWidget');
    if (contactWidget) {
        const toggle = document.getElementById('contactToggle');
        const panel = document.getElementById('socialPanel');
        let isOpen = false;

        // Функция для открытия/закрытия панели
        function togglePanel() {
            isOpen = !isOpen;
            
            if (isOpen) {
                panel.classList.add('contact-widget__panel--active');
                toggle.classList.add('contact-widget__toggle--active');
                toggle.setAttribute('aria-expanded', 'true');
                toggle.setAttribute('aria-label', 'Закрыть контакты');
                
                // Иконки появляются без анимации
            } else {
                panel.classList.remove('contact-widget__panel--active');
                toggle.classList.remove('contact-widget__toggle--active');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.setAttribute('aria-label', 'Открыть контакты');
            }
        }

        // Обработчик клика по основной кнопке
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            togglePanel();
        });

        // Закрытие при клике вне виджета
        document.addEventListener('click', (e) => {
            if (isOpen && !contactWidget.contains(e.target)) {
                togglePanel();
            }
        });

        // Закрытие при нажатии Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isOpen) {
                togglePanel();
            }
        });

        // Hover эффекты для ссылок
        const socialLinks = panel.querySelectorAll('.contact-widget__link');
        socialLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                gsap.to(this, { 
                    scale: 1.1, 
                    duration: 0.2, 
                    ease: "power2.out" 
                });
            });
            
            link.addEventListener('mouseleave', function() {
                gsap.to(this, { 
                    scale: 1, 
                    duration: 0.2, 
                    ease: "power2.out" 
                });
            });
        });

        // Виджет появляется без анимации
    }

    // ========================================================================
    // --- ПРОВЕРКА AMBIENT LIGHT В CARD HEAD 2 БЛОКАХ ---
    // ========================================================================
    const cardHead2Containers = document.querySelectorAll('.card-head-2-container');
    console.log(`Найдено Card Head 2 блоков: ${cardHead2Containers.length}`);
    
    cardHead2Containers.forEach((container, index) => {
        const ambientLight = container.querySelector('.card-head-2-ambient-light');
        const video = container.querySelector('.card-head-2-main-video');
        
        console.log(`Блок ${index + 1}:`, {
            container: !!container,
            ambientLight: !!ambientLight,
            video: !!video,
            videoId: video?.id
        });
        
        if (ambientLight && video) {
            console.log('Ambient Light элемент найден и готов к работе');
            
            // Инициализируем ambient light для этого блока
            initializeAmbientLight(container, video, ambientLight);
        } else {
            console.warn('Ambient Light элемент не найден или видео отсутствует');
        }
    });
});

// ========================================================================
// --- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ AMBIENT LIGHT ---
// ========================================================================
function initializeAmbientLight(container, video, ambientLight) {
    console.log('Инициализация Ambient Light для видео:', video.id);
    
    const canvas = container.querySelector('.card-head-2-color-canvas');
    if (!canvas) {
        console.warn('Canvas не найден для анализа цветов');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    let colorAnalysisInterval;
    let isAnalyzing = false;
    
    // Переменные для плавного смешивания цветов
    let currentColors = {
        primary: [128, 128, 128],   // Текущие цвета (серый по умолчанию)
        secondary: [128, 128, 128],
        tertiary: [128, 128, 128]
    };
    const lerpSpeed = 0.1; // Скорость смешивания
    
    // История цветов для сглаживания
    const colorHistory = {
        primary: [],
        secondary: [],
        tertiary: []
    };
    const maxHistorySize = 5;
    
    // Функция для извлечения доминирующих цветов из видео
    function extractDominantColors() {
        if (!video.videoWidth || !video.videoHeight) return null;
        
        // Устанавливаем размер canvas
        canvas.width = 64; // Маленький размер для быстрого анализа
        canvas.height = 36;
        
        // Рисуем кадр видео на canvas
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Получаем данные пикселей
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        
        // Анализируем цвета
        const colorCounts = {};
        const sampleSize = 4; // Анализируем каждый 4-й пиксель для производительности
        
        for (let i = 0; i < data.length; i += sampleSize * 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            
            // Пропускаем слишком темные и слишком светлые пиксели
            const brightness = (r + g + b) / 3;
            if (brightness < 30 || brightness > 225) continue;
            
            // Квантуем цвета для группировки похожих
            const quantizedR = Math.floor(r / 32) * 32;
            const quantizedG = Math.floor(g / 32) * 32;
            const quantizedB = Math.floor(b / 32) * 32;
            
            const colorKey = `${quantizedR},${quantizedG},${quantizedB}`;
            colorCounts[colorKey] = (colorCounts[colorKey] || 0) + 1;
        }
        
        // Находим доминирующие цвета
        const sortedColors = Object.entries(colorCounts)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 3)
            .map(([color]) => color.split(',').map(Number));
        
        return sortedColors;
    }
    
    // Функция для плавного смешивания цветов (lerp)
    function lerpColor(current, target, t) {
        return [
            Math.round(current[0] + (target[0] - current[0]) * t),
            Math.round(current[1] + (target[1] - current[1]) * t),
            Math.round(current[2] + (target[2] - current[2]) * t)
        ];
    }
    
    // Функция для добавления цвета в историю
    function addColorToHistory(colorType, color) {
        colorHistory[colorType].push([...color]); // Копируем массив
        
        // Ограничиваем размер истории
        if (colorHistory[colorType].length > maxHistorySize) {
            colorHistory[colorType].shift(); // Удаляем самый старый цвет
        }
    }
    
    // Функция для усреднения цветов из истории
    function getAverageColor(colorType) {
        const history = colorHistory[colorType];
        if (history.length === 0) {
            return [128, 128, 128]; // Серый по умолчанию
        }
        
        // Суммируем все цвета
        const sum = [0, 0, 0];
        for (const color of history) {
            sum[0] += color[0];
            sum[1] += color[1];
            sum[2] += color[2];
        }
        
        // Возвращаем среднее значение
        return [
            Math.round(sum[0] / history.length),
            Math.round(sum[1] / history.length),
            Math.round(sum[2] / history.length)
        ];
    }
    
    // Функция для обновления ambient light с плавным смешиванием
    function updateAmbientLight(colors) {
        if (!colors || colors.length === 0) return;
        
        // Получаем новые цвета из видео
        const newPrimary = colors[0];
        const newSecondary = colors[1] || newPrimary;
        const newTertiary = colors[2] || newSecondary;
        
        // Добавляем новые цвета в историю
        addColorToHistory('primary', newPrimary);
        addColorToHistory('secondary', newSecondary);
        addColorToHistory('tertiary', newTertiary);
        
        // Получаем усредненные цвета из истории
        const averagedPrimary = getAverageColor('primary');
        const averagedSecondary = getAverageColor('secondary');
        const averagedTertiary = getAverageColor('tertiary');
        
        // Плавно смешиваем текущие цвета с усредненными
        currentColors.primary = lerpColor(currentColors.primary, averagedPrimary, lerpSpeed);
        currentColors.secondary = lerpColor(currentColors.secondary, averagedSecondary, lerpSpeed);
        currentColors.tertiary = lerpColor(currentColors.tertiary, averagedTertiary, lerpSpeed);
        
        // Создаем RGB строки
        const primaryRgb = `rgb(${currentColors.primary[0]}, ${currentColors.primary[1]}, ${currentColors.primary[2]})`;
        const secondaryRgb = `rgb(${currentColors.secondary[0]}, ${currentColors.secondary[1]}, ${currentColors.secondary[2]})`;
        const tertiaryRgb = `rgb(${currentColors.tertiary[0]}, ${currentColors.tertiary[1]}, ${currentColors.tertiary[2]})`;
        
        // Создаем радиальный градиент
        const gradient = `radial-gradient(ellipse at center, 
            ${primaryRgb} 0%, 
            ${secondaryRgb} 30%, 
            ${tertiaryRgb} 60%, 
            transparent 100%)`;
        
        ambientLight.style.background = gradient;
        ambientLight.classList.add('active');
        
        console.log('Ambient Light обновлен с цветами:', {
            primary: primaryRgb,
            secondary: secondaryRgb,
            tertiary: tertiaryRgb
        });
    }
    
    // Функция для анализа цветов в реальном времени
    function analyzeColors() {
        if (isAnalyzing) return;
        isAnalyzing = true;
        
        const colors = extractDominantColors();
        if (colors) {
            updateAmbientLight(colors);
        }
        
        isAnalyzing = false;
    }
    
    // Автозапуск видео и запуск анализа цветов
    video.addEventListener('canplay', function() {
        video.play().then(() => {
            console.log('Card Head 2 видео запущено с Ambient Light');
            
            // Запускаем анализ цветов 10 раз в секунду (каждые 100ms)
            setTimeout(() => {
                colorAnalysisInterval = setInterval(() => {
                    if (!video.paused && !video.ended) {
                        analyzeColors();
                    }
                }, 100); // 10 раз в секунду
            }, 500);
            
        }).catch((error) => {
            console.warn('Не удалось запустить видео:', error);
        });
    });
    
    // Останавливаем анализ при паузе, но оставляем подсветку
    video.addEventListener('pause', function() {
        if (colorAnalysisInterval) {
            clearInterval(colorAnalysisInterval);
            colorAnalysisInterval = null;
        }
        // Убираем эту строку, чтобы подсветка оставалась включенной
        // ambientLight.classList.remove('active');
    });
    
    // Возобновляем анализ при воспроизведении
    video.addEventListener('play', function() {
        if (!colorAnalysisInterval) {
            colorAnalysisInterval = setInterval(() => {
                if (!video.paused && !video.ended) {
                    analyzeColors();
                }
            }, 100); // 10 раз в секунду
        }
    });
    
    // Очистка при завершении видео
    video.addEventListener('ended', function() {
        if (colorAnalysisInterval) {
            clearInterval(colorAnalysisInterval);
            colorAnalysisInterval = null;
        }
        ambientLight.classList.remove('active');
    });
    
    // Обновляем заголовок страницы
    const projectName = video.getAttribute('data-project-name');
    const projectHeading = document.getElementById('project-heading');
    if (projectHeading && projectName) {
        projectHeading.textContent = projectName;
    }
    
    // Очистка при удалении элемента
    container.addEventListener('beforeunload', function() {
        if (colorAnalysisInterval) {
            clearInterval(colorAnalysisInterval);
            colorAnalysisInterval = null;
        }
    });
}