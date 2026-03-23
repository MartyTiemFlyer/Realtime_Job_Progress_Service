// main.js

const button = document.getElementById('myButton');
const messageDiv = document.createElement('div');
document.body.appendChild(messageDiv);

let clickCount = 0;

// Новая функция для POST-запроса
async function sendPostRequest(data) {
    try {
        const response = await fetch('http://localhost:8000/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        console.log('Ответ сервера:', result);
        return result;
        
    } catch (error) {
        console.error('Ошибка при отправке:', error);
        throw error;
    }
}

// Обновленная функция handleClick с POST-запросом
async function handleClick() {
    clickCount++;
    if (clickCount === 1) {
        messageDiv.textContent = 'Вы нажали на кнопку 1 раз! Отправляю данные...';
    } else {
        messageDiv.textContent = `Вы нажали на кнопку ${clickCount} раз! Отправляю данные...`;
    }
    
    
    try {
        const serverResponse = await sendPostRequest(postData);
        messageDiv.textContent = `Клик ${clickCount}. Сервер ответил: ID ${serverResponse.task_id}`;
        
    } catch (error) {
        messageDiv.textContent = `Ошибка при отправке клика ${clickCount}`;
    }
    
    console.log(`Кнопка нажата. Всего кликов: ${clickCount}`);
}

button.addEventListener('click', handleClick);