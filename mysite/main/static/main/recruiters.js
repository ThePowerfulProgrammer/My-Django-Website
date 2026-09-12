addEventListener("DOMContentLoaded", () => {
    // set up gsap
    gsap.registerPlugin(ScrollTrigger);
       
    const cards = document.getElementsByClassName("card");

    for (let card of cards) {
        card.addEventListener("mouseenter", () => {
            gsap.to(card, {
            y: -8,
            scale: 1.02,
            boxShadow: "0 20px 40px rgba(0,0,0,0.2)",
            duration: 0.3
            });
        });

        card.addEventListener("mouseleave", () => {
            gsap.to(card, {
            y: 0,
            scale: 1,
            boxShadow: "0 10px 20px rgba(0,0,0,0.1)",
            duration: 0.3
            });
        });        
    }

})