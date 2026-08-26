addEventListener("DOMContentLoaded", () => 
    {
        // set up gsap
        gsap.registerPlugin(TextPlugin)
        gsap.registerPlugin(ScrollTrigger);


        // let me set up a helpful message for the user
        let terminalHistory = document.getElementById("terminalHistory")
        terminalHistory.innerHTML = "D:\\ThePowerfulProgrammer> Type 'help' for available commands" + "<br>"

        const routes = document.getElementById("routes")
        const fitnessUrl = routes.dataset.fitness
        const aboutUrl = routes.dataset.about

        // 0) CREATE THE INITIAL COMMANDS
        commands = {
            help: "Available commands: help, apps, about, clear",
            apps: "PotentialUnleashed, PresentsForPeach, OurWatchList",
            clear: "clear",
        }

        apps = {
            potentialunleashed: fitnessUrl, 
            about: aboutUrl
        }


        // set focus

        function setFocus() 
        {
            document.getElementById("commandPrompt").focus();
        }

        setFocus();
        


        // 1) GRAB THE INPUT WIDGET 

        let inputWidget = document.getElementById("commandPrompt");
        
        if (inputWidget != null) 
            {
                // 2) ASSIGN THE STARTING VALUE OF THE WIDGET
                inputWidget.value = "D:\\ThePowerfulProgrammer>";
                
                // 3) ADD EVENTLISTNER

                inputWidget.addEventListener("keydown", (key) =>  {
                    let enter = key.key ;
                    

                    // 4) ONLY RESPOND IF USER HITS ENTER
                    if (enter == "Enter") 
                        {                            
                            // 5)  GRAB POS AFTER >  
                            let arrowPosition = inputWidget.value.search(/>/i) + 1

                            // 6) GRAB TEXT FROM INPUTWIDGET 
                            let text = inputWidget.value.slice(arrowPosition);                             

                            if (text) 
                                {                                    
                                    // Cool Text exists now lets do something
                                    let userCommand = text.toLowerCase();

                                    if (commands[userCommand] == "clear") 
                                    {
                                        let terminalHistory = document.getElementById("terminalHistory")
                                        terminalHistory.innerHTML = "D:\\ThePowerfulProgrammer> Type 'help' for available commands" + "<br>"

                                        // RESET THE INPUTWIDGET VALUE
                                        inputWidget.value = "D:\\ThePowerfulProgrammer>";                                                                                    
                                    }
                                    else if (commands[userCommand]) 
                                        {

                                            

                                            console.log(commands[userCommand])
                                            
                                            // Add input and output to terminal history
                                            let terminalHistory = document.getElementById("terminalHistory")
                                            terminalHistory.innerHTML += inputWidget.value + "<br>" + commands[userCommand] + "<br>"                                            

                                            // auto-scroll to the bottom so the newest line is always visible
                                            terminalHistory.scrollTop = terminalHistory.scrollHeight;                                            

                                            // RESET THE INPUTWIDGET VALUE
                                            inputWidget.value = "D:\\ThePowerfulProgrammer>";                                            
                                        }
                                    else if (apps[userCommand]) 
                                        {
                                            // User is trying to get to a specific app
                                            // I need the route and I need to route the user to that route

                                            window.location.href = apps[userCommand]                                            

                                        }
                                    
                                    else 
                                        {
                                            console.log(text, "is not recognized as an internal or external command, operable program or batch file.")
                                        }
                                    

                                    // RESET THE INPUTWIDGET VALUE
                                    inputWidget.value = "D:\\ThePowerfulProgrammer>";


                                }
                            else 
                                {

                                    // Add input and output to terminal history
                                    let terminalHistory = document.getElementById("terminalHistory")
                                    terminalHistory.innerHTML += "D:\\ThePowerfulProgrammer>"  + "<br>"                                            

                                    // auto-scroll to the bottom so the newest line is always visible
                                    terminalHistory.scrollTop = terminalHistory.scrollHeight;                                            

                                    // RESET THE INPUTWIDGET VALUE
                                    inputWidget.value = "D:\\ThePowerfulProgrammer>";                                       


                                }
                            
                            
                        } 
                    else if (enter === "Backspace") 
                        {
                            if (inputWidget.value.length <= 25) 
                                {
                                    key.preventDefault()
                                }
                        }
                    else if (enter === "Delete") 
                        {
                            key.preventDefault()
                        }
                    else if (enter === "ArrowLeft") 
                        {
                            if (inputWidget.value.length <= 25) 
                                {
                                    key.preventDefault()
                                }                            
                        }
                    else 
                        {
                            // Simple ignore, user has not pressed enter yet
                        }
                })
            }

        else 
            {
                console.log("Cannot find inputWidget");
            }
            



        console.log("OUTSIDE EVENET");

        // GSAP stuff
        gsap.to(".explore", {
            scrambleText: {
                text: "Explore", 
                chars: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                speed: 1
            },
            
            duration: 3.5
        });




    })