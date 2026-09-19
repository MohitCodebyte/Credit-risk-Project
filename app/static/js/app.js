/* =========================================================
   CREDITRISK AI
   PREMIUM INTERACTION & ANIMATION ENGINE
   VERSION 2.0
   ========================================================= */

"use strict";


/* =========================================================
   GLOBAL CONFIG
   ========================================================= */

const CR_CONFIG = {
    animationDuration: 700,
    counterDuration: 1600,
    tiltMax: 8,
    magneticStrength: 0.18,
    mobileBreakpoint: 800
};


/* =========================================================
   DOM READY
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    initPageLoader();

    initScrollReveal();

    initCounters();

    initMobileMenu();

    init3DParallax();

    initAdvanced3DParallax();

    initFormValidation();

    initFormLoading();

    initSmoothNavigation();

    initInputInteractions();

    initNavbar();

    initActiveNavigation();

    initTiltCards();

    initMagneticButtons();

    initButtonRipple();

    initCursorGlow();

    initRiskScoreAnimation();

    initRiskProgress();

    initChartAnimations();

    initFeatureBars();

    initDonutAnimation();

    initDashboardInteractions();

    initResultInteractions();

    initPageTransitions();

    initScrollTop();

    initFloatingParticles();

    initLazyAnimations();

    initAccessibility();

});


/* =========================================================
   PAGE LOADER
   ========================================================= */

function initPageLoader() {

    const loader = document.getElementById("pageLoader");

    if (!loader) {
        return;
    }

    const hideLoader = () => {

        setTimeout(() => {

            loader.classList.add("hidden");

            setTimeout(() => {

                if (loader && loader.parentNode) {
                    loader.remove();
                }

            }, 700);

        }, 500);

    };


    if (document.readyState === "complete") {

        hideLoader();

    } else {

        window.addEventListener(
            "load",
            hideLoader,
            { once: true }
        );

    }

}


/* =========================================================
   SCROLL REVEAL
   ========================================================= */

function initScrollReveal() {

    const elements =
        document.querySelectorAll(
            ".reveal, .reveal-up, .reveal-left, .reveal-right"
        );

    if (!elements.length) {
        return;
    }


    if (!("IntersectionObserver" in window)) {

        elements.forEach(element => {
            element.classList.add("visible");
        });

        return;
    }


    const observer =
        new IntersectionObserver(
            (entries, observerInstance) => {

                entries.forEach(entry => {

                    if (!entry.isIntersecting) {
                        return;
                    }

                    entry.target.classList.add("visible");

                    observerInstance.unobserve(
                        entry.target
                    );

                });

            },
            {
                threshold: 0.1,
                rootMargin: "0px 0px -45px 0px"
            }
        );


    elements.forEach(element => {

        observer.observe(element);

    });

}


/* =========================================================
   STAGGER REVEAL
   ========================================================= */

function initLazyAnimations() {

    const groups = [
        ".process-grid > *",
        ".about-feature-grid > *",
        ".model-grid > *",
        ".formula-grid > *",
        ".dashboard-kpis > *",
        ".risk-scale > *",
        ".tech-stack-large > *",
        ".methodology-timeline > *"
    ];


    groups.forEach(selector => {

        const elements =
            document.querySelectorAll(selector);

        elements.forEach((element, index) => {

            element.style.setProperty(
                "--animation-delay",
                `${Math.min(index * 80, 600)}ms`
            );

        });

    });

}


/* =========================================================
   ANIMATED COUNTERS
   ========================================================= */

function initCounters() {

    const counters =
        document.querySelectorAll(".counter");

    if (!counters.length) {
        return;
    }


    const animateCounter = element => {

        if (element.dataset.counted === "true") {
            return;
        }

        element.dataset.counted = "true";


        const target =
            parseFloat(
                element.dataset.target || "0"
            );

        const format =
            element.dataset.format || "normal";

        const duration =
            Number(
                element.dataset.duration ||
                CR_CONFIG.counterDuration
            );

        const prefix =
            element.dataset.prefix || "";

        const suffix =
            element.dataset.suffix || "";

        const decimals =
            Number(
                element.dataset.decimals ||
                (target % 1 !== 0 ? 2 : 0)
            );


        const startTime =
            performance.now();


        function update(currentTime) {

            const elapsed =
                currentTime - startTime;

            const progress =
                Math.min(
                    elapsed / duration,
                    1
                );


            const eased =
                1 -
                Math.pow(
                    1 - progress,
                    3
                );


            const value =
                target * eased;


            let output;


            if (format === "comma") {

                output =
                    Math.floor(value)
                        .toLocaleString("en-IN");

            } else if (decimals > 0) {

                output =
                    value.toFixed(decimals);

            } else {

                output =
                    Math.floor(value)
                        .toString();

            }


            element.textContent =
                prefix +
                output +
                suffix;


            if (progress < 1) {

                requestAnimationFrame(update);

            } else {

                let finalValue;

                if (format === "comma") {

                    finalValue =
                        Math.floor(target)
                            .toLocaleString("en-IN");

                } else if (decimals > 0) {

                    finalValue =
                        target.toFixed(decimals);

                } else {

                    finalValue =
                        Math.floor(target)
                            .toString();

                }


                element.textContent =
                    prefix +
                    finalValue +
                    suffix;

            }

        }


        requestAnimationFrame(update);

    };


    if (!("IntersectionObserver" in window)) {

        counters.forEach(animateCounter);

        return;
    }


    const observer =
        new IntersectionObserver(
            (entries, observerInstance) => {

                entries.forEach(entry => {

                    if (!entry.isIntersecting) {
                        return;
                    }

                    animateCounter(entry.target);

                    observerInstance.unobserve(
                        entry.target
                    );

                });

            },
            {
                threshold: 0.5
            }
        );


    counters.forEach(counter => {

        observer.observe(counter);

    });

}


/* =========================================================
   MOBILE MENU
   ========================================================= */

function initMobileMenu() {

    const menuButton =
        document.getElementById(
            "mobileMenuBtn"
        );

    const mobileNav =
        document.getElementById(
            "mobileNav"
        );


    if (!menuButton || !mobileNav) {
        return;
    }


    const lines =
        menuButton.querySelectorAll(
            "span"
        );


    const closeMenu = () => {

        mobileNav.classList.remove("open");

        menuButton.setAttribute(
            "aria-expanded",
            "false"
        );


        if (lines.length >= 3) {

            lines[0].style.transform = "";
            lines[1].style.opacity = "";
            lines[2].style.transform = "";

        }

        document.body.classList.remove(
            "mobile-menu-open"
        );

    };


    const openMenu = () => {

        mobileNav.classList.add("open");

        menuButton.setAttribute(
            "aria-expanded",
            "true"
        );


        if (lines.length >= 3) {

            lines[0].style.transform =
                "translateY(7px) rotate(45deg)";

            lines[1].style.opacity = "0";

            lines[2].style.transform =
                "translateY(-7px) rotate(-45deg)";

        }

        document.body.classList.add(
            "mobile-menu-open"
        );

    };


    menuButton.addEventListener(
        "click",
        event => {

            event.stopPropagation();

            const isOpen =
                mobileNav.classList.contains(
                    "open"
                );

            if (isOpen) {
                closeMenu();
            } else {
                openMenu();
            }

        }
    );


    mobileNav
        .querySelectorAll("a")
        .forEach(link => {

            link.addEventListener(
                "click",
                closeMenu
            );

        });


    document.addEventListener(
        "click",
        event => {

            if (
                mobileNav.classList.contains("open") &&
                !mobileNav.contains(event.target) &&
                !menuButton.contains(event.target)
            ) {

                closeMenu();

            }

        }
    );


    document.addEventListener(
        "keydown",
        event => {

            if (event.key === "Escape") {
                closeMenu();
            }

        }
    );

}


/* =========================================================
   BASIC 3D PARALLAX
   ========================================================= */

function init3DParallax() {

    const scene =
        document.getElementById(
            "visualScene"
        );

    if (!scene) {
        return;
    }


    const isTouchDevice =
        window.matchMedia(
            "(hover: none)"
        ).matches;


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (
        isTouchDevice ||
        reducedMotion
    ) {
        return;
    }


    let animationFrame = null;


    document.addEventListener(
        "mousemove",
        event => {

            if (animationFrame) {
                cancelAnimationFrame(
                    animationFrame
                );
            }


            animationFrame =
                requestAnimationFrame(() => {

                    const x =
                        (
                            event.clientX /
                            window.innerWidth
                        ) - 0.5;

                    const y =
                        (
                            event.clientY /
                            window.innerHeight
                        ) - 0.5;


                    const rotateY =
                        x * 8;

                    const rotateX =
                        y * -7;


                    scene.style.transform =
                        `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

                });

        }
    );


    document.addEventListener(
        "mouseleave",
        () => {

            scene.style.transform =
                "rotateX(0deg) rotateY(0deg)";

        }
    );

}


/* =========================================================
   ADVANCED 3D PARALLAX
   ========================================================= */

function initAdvanced3DParallax() {

    const scene =
        document.querySelector(
            ".page-visual-scene"
        );

    if (!scene) {
        return;
    }


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    const touch =
        window.matchMedia(
            "(hover: none)"
        ).matches;


    if (reducedMotion || touch) {
        return;
    }


    let raf = null;


    document.addEventListener(
        "mousemove",
        event => {

            if (raf) {
                cancelAnimationFrame(raf);
            }


            raf =
                requestAnimationFrame(() => {

                    const x =
                        (
                            event.clientX /
                            window.innerWidth
                        ) - 0.5;

                    const y =
                        (
                            event.clientY /
                            window.innerHeight
                        ) - 0.5;


                    const rotateX =
                        y * -8;

                    const rotateY =
                        x * 10;


                    scene.style.transform =
                        `
                        translateY(-5px)
                        rotateX(${rotateX}deg)
                        rotateY(${rotateY}deg)
                        `;

                });

        }
    );


    document.addEventListener(
        "mouseleave",
        () => {

            scene.style.transform =
                "";

        }
    );

}


/* =========================================================
   FORM VALIDATION
   ========================================================= */

function initFormValidation() {

    const form =
        document.getElementById(
            "riskForm"
        );

    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        event => {

            let valid = true;

            let firstInvalidField = null;


            const requiredFields =
                form.querySelectorAll(
                    "input[required], select[required]"
                );


            requiredFields.forEach(field => {

                const value =
                    String(
                        field.value || ""
                    ).trim();


                field.classList.remove(
                    "input-error"
                );


                if (!value) {

                    valid = false;

                    field.classList.add(
                        "input-error"
                    );


                    if (!firstInvalidField) {
                        firstInvalidField =
                            field;
                    }

                }

            });


            validateRange(
                form,
                "credit_score",
                300,
                900,
                value => `Credit score must be between 300 and 900.`,
                state => state
            );


            const creditScore =
                document.getElementById(
                    "credit_score"
                );


            if (
                creditScore &&
                creditScore.value !== ""
            ) {

                const score =
                    Number(
                        creditScore.value
                    );


                if (
                    score < 300 ||
                    score > 900
                ) {

                    valid = false;

                    creditScore.classList.add(
                        "input-error"
                    );


                    if (!firstInvalidField) {
                        firstInvalidField =
                            creditScore;
                    }

                }

            }


            const age =
                document.getElementById(
                    "age"
                );


            if (
                age &&
                age.value !== ""
            ) {

                const ageValue =
                    Number(age.value);


                if (
                    ageValue < 18 ||
                    ageValue > 100
                ) {

                    valid = false;

                    age.classList.add(
                        "input-error"
                    );


                    if (!firstInvalidField) {
                        firstInvalidField =
                            age;
                    }

                }

            }


            const monthlyIncome =
                document.getElementById(
                    "monthly_income"
                );

            const annualIncome =
                document.getElementById(
                    "annual_income"
                );


            if (
                monthlyIncome &&
                annualIncome &&
                monthlyIncome.value &&
                annualIncome.value
            ) {

                const monthly =
                    Number(
                        monthlyIncome.value
                    );

                const annual =
                    Number(
                        annualIncome.value
                    );


                if (
                    monthly <= 0 ||
                    annual <= 0
                ) {

                    valid = false;

                    monthlyIncome.classList.add(
                        "input-error"
                    );


                    annualIncome.classList.add(
                        "input-error"
                    );


                    if (!firstInvalidField) {
                        firstInvalidField =
                            monthlyIncome;
                    }

                }

            }


            if (!valid) {

                event.preventDefault();


                if (firstInvalidField) {

                    firstInvalidField.focus();

                    firstInvalidField.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                }


                showFormMessage(
                    "Please check the highlighted fields.",
                    "error"
                );

            }

        }
    );


    form
        .querySelectorAll(
            "input, select"
        )
        .forEach(field => {

            field.addEventListener(
                "input",
                () => {

                    field.classList.remove(
                        "input-error"
                    );

                }
            );


            field.addEventListener(
                "change",
                () => {

                    field.classList.remove(
                        "input-error"
                    );

                }
            );

        });

}


/* =========================================================
   RANGE VALIDATOR HELPER
   ========================================================= */

function validateRange(
    form,
    id,
    min,
    max,
    message,
    callback
) {

    const field =
        document.getElementById(id);

    if (!field) {
        return true;
    }


    if (!field.value) {
        return true;
    }


    const value =
        Number(field.value);


    if (
        value < min ||
        value > max
    ) {

        field.classList.add(
            "input-error"
        );

        return false;

    }


    return true;
}


/* =========================================================
   FORM LOADING
   ========================================================= */

function initFormLoading() {

    const form =
        document.getElementById(
            "riskForm"
        );

    const submitButton =
        document.getElementById(
            "submitBtn"
        );


    if (!form || !submitButton) {
        return;
    }


    form.addEventListener(
        "submit",
        () => {

            setTimeout(() => {

                if (
                    form.checkValidity()
                ) {

                    submitButton.classList.add(
                        "loading"
                    );

                    submitButton.disabled =
                        true;

                    const originalHTML =
                        submitButton.innerHTML;


                    submitButton.dataset.original =
                        originalHTML;


                    submitButton.innerHTML = `
                        <span class="btn-loading-spinner"></span>
                        <span>Analyzing Risk...</span>
                    `;

                }

            }, 60);

        }
    );

}


/* =========================================================
   SMOOTH NAVIGATION
   ========================================================= */

function initSmoothNavigation() {

    const links =
        document.querySelectorAll(
            'a[href^="#"]'
        );


    links.forEach(link => {

        link.addEventListener(
            "click",
            event => {

                const targetId =
                    link.getAttribute(
                        "href"
                    );


                if (
                    !targetId ||
                    targetId === "#"
                ) {
                    return;
                }


                const target =
                    document.querySelector(
                        targetId
                    );


                if (!target) {
                    return;
                }


                event.preventDefault();


                const navbar =
                    document.querySelector(
                        ".navbar-wrapper"
                    );


                const navbarHeight =
                    navbar
                        ? navbar.offsetHeight + 20
                        : 20;


                const targetPosition =
                    target.getBoundingClientRect()
                        .top +
                    window.scrollY -
                    navbarHeight;


                window.scrollTo({
                    top: targetPosition,
                    behavior: "smooth"
                });


                history.replaceState(
                    null,
                    "",
                    targetId
                );

            }
        );

    });

}


/* =========================================================
   INPUT INTERACTIONS
   ========================================================= */

function initInputInteractions() {

    const inputs =
        document.querySelectorAll(
            ".input-wrapper input, .input-wrapper select, .field input, .field select"
        );


    inputs.forEach(input => {

        input.addEventListener(
            "focus",
            () => {

                const wrapper =
                    input.closest(
                        ".input-wrapper, .field"
                    );


                if (wrapper) {

                    wrapper.classList.add(
                        "focused"
                    );

                }

            }
        );


        input.addEventListener(
            "blur",
            () => {

                const wrapper =
                    input.closest(
                        ".input-wrapper, .field"
                    );


                if (wrapper) {

                    wrapper.classList.remove(
                        "focused"
                    );

                }

            }
        );

    });


    initCreditScoreFeedback();

}


/* =========================================================
   CREDIT SCORE FEEDBACK
   ========================================================= */

function initCreditScoreFeedback() {

    const creditScore =
        document.getElementById(
            "credit_score"
        );


    if (!creditScore) {
        return;
    }


    creditScore.addEventListener(
        "input",
        () => {

            const value =
                Number(
                    creditScore.value
                );


            const field =
                creditScore.closest(
                    ".field"
                );


            if (!field) {
                return;
            }


            if (value >= 750) {

                field.dataset.scoreState =
                    "excellent";

            } else if (value >= 650) {

                field.dataset.scoreState =
                    "good";

            } else if (value >= 550) {

                field.dataset.scoreState =
                    "fair";

            } else if (value > 0) {

                field.dataset.scoreState =
                    "low";

            } else {

                field.dataset.scoreState =
                    "";

            }

        }
    );

}


/* =========================================================
   FORM MESSAGE
   ========================================================= */

function showFormMessage(
    message,
    type = "error"
) {

    const existing =
        document.querySelector(
            ".js-form-message"
        );


    if (existing) {
        existing.remove();
    }


    const element =
        document.createElement(
            "div"
        );


    element.className =
        `js-form-message ${type}`;


    const icon =
        type === "error"
            ? "fa-triangle-exclamation"
            : "fa-circle-check";


    element.innerHTML = `
        <div class="js-form-message-icon">
            <i class="fa-solid ${icon}"></i>
        </div>

        <span>
            ${escapeHtml(message)}
        </span>
    `;


    const form =
        document.getElementById(
            "riskForm"
        );


    if (!form) {
        return;
    }


    form.prepend(element);


    requestAnimationFrame(() => {

        element.classList.add(
            "visible"
        );

    });


    setTimeout(() => {

        element.classList.remove(
            "visible"
        );


        setTimeout(() => {

            if (element.parentNode) {
                element.remove();
            }

        }, 300);

    }, 4500);

}


/* =========================================================
   ESCAPE HTML
   ========================================================= */

function escapeHtml(value) {

    return String(value)
        .replaceAll(
            "&",
            "&amp;"
        )
        .replaceAll(
            "<",
            "&lt;"
        )
        .replaceAll(
            ">",
            "&gt;"
        )
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );

}


/* =========================================================
   NAVBAR
   ========================================================= */

function initNavbar() {

    const navbar =
        document.querySelector(
            ".navbar"
        );


    if (!navbar) {
        return;
    }


    const updateNavbar =
        () => {

            if (
                window.scrollY > 20
            ) {

                navbar.classList.add(
                    "scrolled"
                );

                navbar.style.boxShadow =
                    "0 15px 40px rgba(15, 23, 42, 0.09)";

            } else {

                navbar.classList.remove(
                    "scrolled"
                );

                navbar.style.boxShadow =
                    "0 12px 35px rgba(15, 23, 42, 0.06)";

            }

        };


    updateNavbar();


    window.addEventListener(
        "scroll",
        updateNavbar,
        {
            passive: true
        }
    );

}


/* =========================================================
   ACTIVE NAVIGATION
   ========================================================= */

function initActiveNavigation() {

    const currentPath =
        window.location.pathname
            .replace(/\/$/, "") ||
        "/";


    document
        .querySelectorAll(
            ".navbar a, .mobile-nav a"
        )
        .forEach(link => {

            const href =
                link.getAttribute("href");


            if (
                !href ||
                href.startsWith("#")
            ) {
                return;
            }


            try {

                const url =
                    new URL(
                        href,
                        window.location.origin
                    );


                const linkPath =
                    url.pathname
                        .replace(/\/$/, "") ||
                    "/";


                if (
                    linkPath === currentPath
                ) {

                    link.classList.add(
                        "active"
                    );

                }

            } catch (error) {
                // Ignore invalid links.
            }

        });

}


/* =========================================================
   3D TILT CARDS
   ========================================================= */

function initTiltCards() {

    const cards =
        document.querySelectorAll(
            ".tilt-card, .about-feature-card, .model-card, .kpi-card, .result-metric-card"
        );


    if (!cards.length) {
        return;
    }


    const touch =
        window.matchMedia(
            "(hover: none)"
        ).matches;


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (
        touch ||
        reducedMotion
    ) {
        return;
    }


    cards.forEach(card => {

        card.addEventListener(
            "mousemove",
            event => {

                const rect =
                    card.getBoundingClientRect();


                const x =
                    event.clientX -
                    rect.left;

                const y =
                    event.clientY -
                    rect.top;


                const centerX =
                    rect.width / 2;

                const centerY =
                    rect.height / 2;


                const rotateY =
                    (
                        (x - centerX) /
                        centerX
                    ) *
                    CR_CONFIG.tiltMax;


                const rotateX =
                    -(
                        (y - centerY) /
                        centerY
                    ) *
                    CR_CONFIG.tiltMax;


                card.style.transform =
                    `
                    perspective(900px)
                    rotateX(${rotateX}deg)
                    rotateY(${rotateY}deg)
                    translateY(-5px)
                    scale(1.01)
                    `;

            }
        );


        card.addEventListener(
            "mouseleave",
            () => {

                card.style.transform =
                    "";

            }
        );

    });

}


/* =========================================================
   MAGNETIC BUTTONS
   ========================================================= */

function initMagneticButtons() {

    const buttons =
        document.querySelectorAll(
            ".magnetic, .btn-primary, .page-primary-btn"
        );


    const touch =
        window.matchMedia(
            "(hover: none)"
        ).matches;


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (
        touch ||
        reducedMotion
    ) {
        return;
    }


    buttons.forEach(button => {

        button.addEventListener(
            "mousemove",
            event => {

                const rect =
                    button.getBoundingClientRect();


                const x =
                    event.clientX -
                    rect.left -
                    rect.width / 2;

                const y =
                    event.clientY -
                    rect.top -
                    rect.height / 2;


                button.style.transform =
                    `
                    translate(
                        ${x * CR_CONFIG.magneticStrength}px,
                        ${y * CR_CONFIG.magneticStrength}px
                    )
                    `;

            }
        );


        button.addEventListener(
            "mouseleave",
            () => {

                button.style.transform =
                    "";

            }
        );

    });

}


/* =========================================================
   BUTTON RIPPLE
   ========================================================= */

function initButtonRipple() {

    const buttons =
        document.querySelectorAll(
            ".btn-primary, .btn-secondary, .page-primary-btn, .page-secondary-btn, .outline-btn"
        );


    buttons.forEach(button => {

        button.addEventListener(
            "click",
            event => {

                const rect =
                    button.getBoundingClientRect();


                const ripple =
                    document.createElement(
                        "span"
                    );


                ripple.className =
                    "button-ripple";


                const size =
                    Math.max(
                        rect.width,
                        rect.height
                    );


                ripple.style.width =
                    `${size}px`;

                ripple.style.height =
                    `${size}px`;


                ripple.style.left =
                    `${event.clientX - rect.left - size / 2}px`;

                ripple.style.top =
                    `${event.clientY - rect.top - size / 2}px`;


                button.appendChild(
                    ripple
                );


                setTimeout(() => {

                    ripple.remove();

                }, 650);

            }
        );

    });

}


/* =========================================================
   CURSOR GLOW
   ========================================================= */

function initCursorGlow() {

    const touch =
        window.matchMedia(
            "(hover: none)"
        ).matches;


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (
        touch ||
        reducedMotion
    ) {
        return;
    }


    const glow =
        document.createElement(
            "div"
        );


    glow.className =
        "cursor-glow";


    document.body.appendChild(
        glow
    );


    let raf = null;


    document.addEventListener(
        "mousemove",
        event => {

            if (raf) {
                cancelAnimationFrame(raf);
            }


            raf =
                requestAnimationFrame(() => {

                    glow.style.left =
                        `${event.clientX}px`;

                    glow.style.top =
                        `${event.clientY}px`;

                    glow.classList.add(
                        "visible"
                    );

                });

        }
    );


    document.addEventListener(
        "mouseleave",
        () => {

            glow.classList.remove(
                "visible"
            );

        }
    );

}


/* =========================================================
   RESULT RISK SCORE ANIMATION
   ========================================================= */

function initRiskScoreAnimation() {

    const scoreElements =
        document.querySelectorAll(
            ".result-score-number, [data-risk-score]"
        );


    if (!scoreElements.length) {
        return;
    }


    scoreElements.forEach(element => {

        let raw =
            element.dataset.riskScore;


        if (!raw) {

            raw =
                element.textContent
                    .replace(
                        /[^0-9.]/g,
                        ""
                    );

        }


        const target =
            parseFloat(raw);


        if (
            Number.isNaN(target)
        ) {
            return;
        }


        const duration = 1400;

        const start =
            performance.now();


        function animate(now) {

            const progress =
                Math.min(
                    (now - start) /
                    duration,
                    1
                );


            const eased =
                1 -
                Math.pow(
                    1 - progress,
                    3
                );


            const value =
                target * eased;


            element.textContent =
                value.toFixed(2);


            if (
                progress < 1
            ) {

                requestAnimationFrame(
                    animate
                );

            } else {

                element.textContent =
                    target.toFixed(2);

            }

        }


        requestAnimationFrame(
            animate
        );

    });

}


/* =========================================================
   RISK PROGRESS
   ========================================================= */

function initRiskProgress() {

    const bars =
        document.querySelectorAll(
            ".risk-progress-fill"
        );


    if (!bars.length) {
        return;
    }


    bars.forEach(bar => {

        let width =
            bar.dataset.width ||
            bar.style.getPropertyValue(
                "--risk-width"
            );


        if (
            !width &&
            bar.closest(".risk-progress")
        ) {

            const valueElement =
                bar.closest(
                    ".risk-progress"
                )
                ?.querySelector(
                    "[data-risk-value]"
                );


            if (valueElement) {

                width =
                    `${parseFloat(
                        valueElement.dataset.riskValue
                    )}%`;

            }

        }


        if (!width) {
            width = "50%";
        }


        bar.style.setProperty(
            "--risk-width",
            "0%"
        );


        requestAnimationFrame(() => {

            setTimeout(() => {

                bar.style.setProperty(
                    "--risk-width",
                    width
                );

            }, 180);

        });

    });

}


/* =========================================================
   CHART BAR ANIMATION
   ========================================================= */

function initChartAnimations() {

    const bars =
        document.querySelectorAll(
            ".chart-bar"
        );


    if (!bars.length) {
        return;
    }


    bars.forEach(
        (bar, index) => {

            const height =
                bar.dataset.height ||
                bar.style.getPropertyValue(
                    "--bar-height"
                ) ||
                "50%";


            bar.style.setProperty(
                "--bar-height",
                height
            );


            bar.style.animationDelay =
                `${index * 80}ms`;

        }
    );

}


/* =========================================================
   FEATURE IMPORTANCE BARS
   ========================================================= */

function initFeatureBars() {

    const bars =
        document.querySelectorAll(
            ".feature-fill"
        );


    bars.forEach(
        (bar, index) => {

            const width =
                bar.dataset.width ||
                bar.style.getPropertyValue(
                    "--feature-width"
                ) ||
                "50%";


            bar.style.setProperty(
                "--feature-width",
                "0%"
            );


            bar.style.animationDelay =
                `${index * 100}ms`;


            requestAnimationFrame(() => {

                setTimeout(() => {

                    bar.style.setProperty(
                        "--feature-width",
                        width
                    );

                }, 250 + index * 70);

            });

        }
    );

}


/* =========================================================
   DONUT ANIMATION
   ========================================================= */

function initDonutAnimation() {

    const donuts =
        document.querySelectorAll(
            ".risk-donut"
        );


    donuts.forEach(donut => {

        donut.style.opacity = "0";

        donut.style.transform =
            "scale(.75) rotate(-25deg)";


        requestAnimationFrame(() => {

            setTimeout(() => {

                donut.style.transition =
                    `
                    opacity .8s ease,
                    transform .9s cubic-bezier(.22,1,.36,1)
                    `;

                donut.style.opacity =
                    "1";

                donut.style.transform =
                    "scale(1) rotate(0deg)";

            }, 200);

        });

    });

}


/* =========================================================
   DASHBOARD INTERACTIONS
   ========================================================= */

function initDashboardInteractions() {

    const dashboard =
        document.querySelector(
            ".dashboard-section"
        );


    if (!dashboard) {
        return;
    }


    const cards =
        dashboard.querySelectorAll(
            ".dashboard-card"
        );


    cards.forEach(card => {

        card.addEventListener(
            "mouseenter",
            () => {

                card.classList.add(
                    "dashboard-card-active"
                );

            }
        );


        card.addEventListener(
            "mouseleave",
            () => {

                card.classList.remove(
                    "dashboard-card-active"
                );

            }
        );

    });


    initChartHover();

}


/* =========================================================
   CHART HOVER
   ========================================================= */

function initChartHover() {

    const bars =
        document.querySelectorAll(
            ".chart-bar"
        );


    bars.forEach(bar => {

        bar.addEventListener(
            "mouseenter",
            () => {

                const value =
                    bar.dataset.value;


                if (!value) {
                    return;
                }


                let tooltip =
                    document.createElement(
                        "div"
                    );


                tooltip.className =
                    "chart-tooltip";


                tooltip.textContent =
                    value;


                bar.appendChild(
                    tooltip
                );

            }
        );


        bar.addEventListener(
            "mouseleave",
            () => {

                const tooltip =
                    bar.querySelector(
                        ".chart-tooltip"
                    );


                if (tooltip) {
                    tooltip.remove();
                }

            }
        );

    });

}


/* =========================================================
   RESULT INTERACTIONS
   ========================================================= */

function initResultInteractions() {

    const result =
        document.querySelector(
            ".result-section"
        );


    if (!result) {
        return;
    }


    const category =
        result.querySelector(
            ".result-score-category"
        );


    if (category) {

        setTimeout(() => {

            category.classList.add(
                "result-category-visible"
            );

        }, 800);

    }


    const metrics =
        result.querySelectorAll(
            ".result-metric-card"
        );


    metrics.forEach(
        (metric, index) => {

            metric.style.transitionDelay =
                `${index * 70}ms`;

        }
    );

}


/* =========================================================
   PAGE TRANSITIONS
   ========================================================= */

function initPageTransitions() {

    const links =
        document.querySelectorAll(
            "a"
        );


    links.forEach(link => {

        link.addEventListener(
            "click",
            event => {

                const href =
                    link.getAttribute(
                        "href"
                    );


                if (
                    !href ||
                    href.startsWith("#") ||
                    href.startsWith("javascript:") ||
                    link.target === "_blank" ||
                    event.ctrlKey ||
                    event.metaKey ||
                    event.shiftKey ||
                    event.altKey
                ) {
                    return;
                }


                let url;


                try {

                    url =
                        new URL(
                            href,
                            window.location.href
                        );

                } catch (error) {

                    return;

                }


                if (
                    url.origin !==
                    window.location.origin
                ) {
                    return;
                }


                const transition =
                    document.querySelector(
                        ".page-transition"
                    );


                if (!transition) {
                    return;
                }


                event.preventDefault();


                transition.classList.add(
                    "active"
                );


                setTimeout(() => {

                    window.location.href =
                        url.href;

                }, 450);

            }
        );

    });

}


/* =========================================================
   SCROLL TO TOP
   ========================================================= */

function initScrollTop() {

    let button =
        document.querySelector(
            ".scroll-top"
        );


    if (!button) {

        button =
            document.createElement(
                "button"
            );

        button.type =
            "button";

        button.className =
            "scroll-top";

        button.setAttribute(
            "aria-label",
            "Scroll to top"
        );

        button.innerHTML =
            `<i class="fa-solid fa-arrow-up"></i>`;

        document.body.appendChild(
            button
        );

    }


    const update =
        () => {

            if (
                window.scrollY >
                500
            ) {

                button.classList.add(
                    "visible"
                );

            } else {

                button.classList.remove(
                    "visible"
                );

            }

        };


    update();


    window.addEventListener(
        "scroll",
        update,
        {
            passive: true
        }
    );


    button.addEventListener(
        "click",
        () => {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        }
    );

}


/* =========================================================
   FLOATING PARTICLES
   ========================================================= */

function initFloatingParticles() {

    const containers =
        document.querySelectorAll(
            ".particles-container, .page-shell, .hero"
        );


    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (reducedMotion) {
        return;
    }


    containers.forEach(container => {

        if (
            container.querySelector(
                ".data-particle"
            )
        ) {
            return;
        }


        for (
            let i = 0;
            i < 5;
            i++
        ) {

            const particle =
                document.createElement(
                    "span"
                );


            particle.className =
                "data-particle";


            particle.style.left =
                `${10 + Math.random() * 80}%`;

            particle.style.top =
                `${10 + Math.random() * 75}%`;


            particle.style.animationDelay =
                `${Math.random() * -6}s`;


            particle.style.animationDuration =
                `${5 + Math.random() * 5}s`;


            container.appendChild(
                particle
            );

        }

    });

}


/* =========================================================
   KEYBOARD ACCESSIBILITY
   ========================================================= */

function initAccessibility() {

    document.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Tab"
            ) {

                document.body.classList.add(
                    "keyboard-navigation"
                );

            }

        }
    );


    document.addEventListener(
        "mousedown",
        () => {

            document.body.classList.remove(
                "keyboard-navigation"
            );

        }
    );

}


/* =========================================================
   PAGESHOW RESET
   ========================================================= */

window.addEventListener(
    "pageshow",
    () => {

        const button =
            document.getElementById(
                "submitBtn"
            );


        if (button) {

            button.disabled =
                false;

            button.classList.remove(
                "loading"
            );


            if (
                button.dataset.original
            ) {

                button.innerHTML =
                    button.dataset.original;

            }

        }


        const transition =
            document.querySelector(
                ".page-transition"
            );


        if (transition) {

            transition.classList.remove(
                "active"
            );

        }

    }
);


/* =========================================================
   WINDOW RESIZE
   ========================================================= */

let resizeTimer = null;


window.addEventListener(
    "resize",
    () => {

        clearTimeout(
            resizeTimer
        );


        resizeTimer =
            setTimeout(() => {

                const isMobile =
                    window.innerWidth <=
                    CR_CONFIG.mobileBreakpoint;


                if (isMobile) {

                    document.body.classList.add(
                        "is-mobile"
                    );

                } else {

                    document.body.classList.remove(
                        "is-mobile"
                    );

                }

            }, 150);

    },
    {
        passive: true
    }
);


/* =========================================================
   INITIAL DEVICE STATE
   ========================================================= */

if (
    window.innerWidth <=
    CR_CONFIG.mobileBreakpoint
) {

    document.body.classList.add(
        "is-mobile"
    );

}


/* =========================================================
   END OF PREMIUM ENGINE
   ========================================================= */