document.addEventListener("DOMContentLoaded", function () {
    const chatboxButton = document.getElementById("chatbox-button");
    const chatboxSupport = document.querySelector(".chatbox__support");
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");

    if (chatboxButton && chatboxSupport) {
        chatboxButton.addEventListener("click", function () {
            chatboxSupport.classList.toggle("chatbox--active");
        });
    } else {
        console.error("❌ عنصر الزر أو صندوق الدردشة غير موجود!");
    }

    if (!chatForm) {
        console.error("❌ نموذج الدردشة غير موجود! تأكد من أن لديك <form id='chat-form'> في HTML.");
        return;
    }

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const userMessage = chatInput.value.trim();

        if (userMessage !== "") {
            const userMessageWrapper = document.createElement("div");
            userMessageWrapper.style.display = "flex";
            userMessageWrapper.style.justifyContent = "flex-end";

            const userMessageElement = document.createElement("div");
            userMessageElement.classList.add("user-message");
            userMessageElement.style.cssText = "background: #581B98; color: white; padding: 8px 12px; border-radius: 15px; max-width: 70%; margin: 5px 0; text-align: right; align-self: flex-end;";
            userMessageElement.innerHTML = `<strong>أنت:</strong> ${userMessage}`;
            
            userMessageWrapper.appendChild(userMessageElement);
            chatMessages.appendChild(userMessageWrapper);
            chatInput.value = "";

            console.log("📤 إرسال الطلب إلى السيرفر:", userMessage); // Debugging
            
            fetch("http://127.0.0.1:8080/get_response", {
                method: "POST",
                body: JSON.stringify({ message: userMessage }),
                headers: { "Content-Type": "application/json" }
            })
            .then(response => {
                console.log("🔄 استجابة السيرفر:", response); // Debugging
                if (!response.ok) {
                    throw new Error("خطأ في الاتصال بالسيرفر");
                }
                return response.json();
            })
            .then(data => {
                console.log("✅ بيانات الرد من السيرفر:", data); // Debugging
                
                const botMessageWrapper = document.createElement("div");
                botMessageWrapper.style.display = "flex";
                botMessageWrapper.style.justifyContent = "flex-start";

                const botMessageElement = document.createElement("div");
                botMessageElement.classList.add("bot-message");
                botMessageElement.style.cssText = "background: #9C1DE7; color: white; padding: 8px 12px; border-radius: 15px; max-width: 70%; margin: 5px 0; text-align: left; align-self: flex-start;";
                botMessageElement.innerHTML = `<strong>البوت:</strong> ${data.response}`;
                
                botMessageWrapper.appendChild(botMessageElement);
                chatMessages.appendChild(botMessageWrapper);
                
                chatMessages.scrollTop = chatMessages.scrollHeight; // جعل الرسائل تظهر بالترتيب الصحيح
            })
            .catch(error => {
                console.error("❌ خطأ أثناء إرسال الطلب:", error);
                const errorMessageElement = document.createElement("div");
                errorMessageElement.classList.add("bot-message", "error");
                errorMessageElement.innerHTML = "❌ حدث خطأ في الاتصال!";
                chatMessages.appendChild(errorMessageElement);
            });
        }
    });
});