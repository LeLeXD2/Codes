const chatArea = document.getElementById("chat-area");

const input = document.getElementById("question");

const sendButton = document.getElementById("send");

let isLoading = false;
let currentController = null;

// ======================================
// Add User Bubble
// ======================================

function addUserMessage(text){

    const message = document.createElement("div");

    message.className = "message user";

    message.innerHTML = `

        <div class="bubble">

            ${text}

        </div>

    `;

    chatArea.appendChild(message);

    chatArea.scrollTop = chatArea.scrollHeight;

}

// ======================================
// Add Bot Bubble
// ======================================

function addBotMessage(html){

    const message = document.createElement("div");

    message.className = "message bot";

    message.innerHTML = `

        <div class="bubble">

            ${html}

        </div>

    `;

    chatArea.appendChild(message);

    chatArea.scrollTop = chatArea.scrollHeight;

}

function addThinkingMessage(){

    const message =
        document.createElement("div");

    message.className =
        "message bot thinking-message";

    message.innerHTML = `

        <div class="bubble">

            🤖 Analysing...

        </div>

    `;

    chatArea.appendChild(message);

    chatArea.scrollTop =
        chatArea.scrollHeight;

}
// ======================================
// Analyse
// ======================================

async function analyse(){

    if(isLoading)
        return;


    const message =
        input.value.trim();

    if(message === "")
        return;


    const welcome =
        document.querySelector(".welcome");

    if(welcome)
        welcome.remove();


    addUserMessage(message);

    input.value = "";


    // ======================================
    // START LOADING
    // ======================================

    isLoading = true;

    currentController =
        new AbortController();

    input.disabled = true;

    sendButton.textContent = "■";

    sendButton.title =
        "Stop generating";


    addThinkingMessage();


    try{

        const response =
            await fetch(
                "/predict",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },

                    body:
                        "message=" +
                        encodeURIComponent(message),

                    signal:
                        currentController.signal

                }
            );


        const data =
            await response.json();


        const thinkingBubble =
            chatArea.querySelector(
                ".thinking-message"
            );

        if(thinkingBubble){
            thinkingBubble.remove();
        }


        // Only show the reply if
        // request wasn't cancelled
        if(isLoading){

            addBotMessage(
                data.reply
            );

        }

    }

    catch(error){

        if(error.name !== "AbortError"){

            const thinkingBubble =
                chatArea.querySelector(
                    ".thinking-message"
                );

            if(thinkingBubble){
                thinkingBubble.remove();
            }

            addBotMessage(
                "Unable to connect to server."
            );

            console.error(error);

        }

    }

    finally{

        // Only reset if this request
        // is still considered active
        if(isLoading){

            isLoading = false;

            currentController = null;

            input.disabled = false;

            sendButton.textContent =
                "➜";

            sendButton.title =
                "Send message";

            input.focus();

        }

    }

}

// ======================================
// Stop Generation
// ======================================
function stopGeneration(){

    if(currentController){

        currentController.abort();

        currentController = null;

    }

    isLoading = false;

    input.disabled = false;

    sendButton.textContent = "➜";

    sendButton.title = "Send message";

    const thinkingBubble =
        chatArea.querySelector(".thinking-message");

    if(thinkingBubble){
        thinkingBubble.remove();
    }

    addBotMessage(
        "⏹ Generation stopped."
    );

    input.focus();

}

// ======================================
// Button
// ======================================
sendButton.addEventListener(
    "click",
    function(){

        if(isLoading){

            stopGeneration();

        }

        else{

            analyse();

        }

    }
);

// ======================================
// Enter
// ======================================

input.addEventListener(
    "keydown",
    function(event){

        if(event.key === "Enter"){

            event.preventDefault();

            if(!isLoading){

                analyse();

            }

        }

    }
);
// ======================================
// NEW CHAT
// ======================================

document
    .getElementById("new-chat")
    .addEventListener("click", async function () {

        try {

            const response = await fetch("/new_chat", {

                method: "POST"

            });

            const data = await response.json();

            if (data.success) {

                resetChat();

            }

        } catch (error) {

            console.error(
                "Unable to start new chat:",
                error
            );

        }

    });

function resetChat() {
    // Add welcome screen
    chatArea.innerHTML = `
            <div class="welcome">

                <h2>How can I help you invest today?</h2>

                <p>Ask me about any stock.</p>

            </div>

    `;

    // Focus input
    input.focus();

}

const sidebar =
    document.getElementById("sidebar");

const main =
    document.getElementById("main");

const openSidebar =
    document.getElementById("open-sidebar");

const closeSidebar =
    document.getElementById("close-sidebar");


function showSidebar() {

    sidebar.classList.add("open");

    main.classList.add("sidebar-open");

}


function hideSidebar() {

    sidebar.classList.remove("open");

    main.classList.remove("sidebar-open");

}


openSidebar.addEventListener(
    "click",
    showSidebar
);


closeSidebar.addEventListener(
    "click",
    hideSidebar
);