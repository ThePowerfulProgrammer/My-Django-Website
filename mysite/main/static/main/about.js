addEventListener("DOMContentLoaded", () => {
    // set up gsap
    gsap.registerPlugin(ScrollTrigger);
    
    
    gsap.from(".grid-item", {
    scale: 0, opacity: 0,
    duration: 0.4,
    stagger: { amount: 0.6, from: "center" },
    ease: "back.out(1.7)",
    scrollTrigger: ".grid"
    });    

    console.log("IN JS FILE")


    // Gravity text
    const chars = SplitText.create(".gravity", {type: 'chars'});
    chars.chars.forEach(ch => {
    gsap.from(ch, {
        y: -200, opacity: 0,
        duration: 0.8, ease: "bounce.out",
        delay: Math.random() * 0.5
    });    
    })

})