// ============================================
// БИБЛИОТЕКА — JavaScript
// ============================================

const API_URL = 'http://127.0.0.1:8000/api';

// ---------- Утилиты ----------
function getToken() {
    return localStorage.getItem('access_token');
}

function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// ---------- Fetch с авторизацией ----------
async function apiFetch(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    // Автоматическое обновление токена
    if (response.status === 401) {
        const refreshed = await refreshToken();
        if (refreshed) {
            return apiFetch(endpoint, options);
        } else {
            clearTokens();
            window.location.href = '/login/';
            throw new Error('Unauthorized');
        }
    }

    if (!response.ok) {
        const error = await response.json();
        throw { response: { data: error, status: response.status } };
    }

    return response.json();
}

// ---------- Обновление токена ----------
async function refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return false;

    try {
        const response = await fetch(`${API_URL}/auth/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        }
    } catch (e) {
        console.error('Refresh failed:', e);
    }
    return false;
}

// ============================================
// НАВИГАЦИЯ — обновление статуса пользователя
// ============================================
function updateAuthNav() {
    const container = document.getElementById('auth-nav');
    if (!container) return;

    const user = getUser();

    if (user) {
        container.innerHTML = `
            <span style="color: var(--gold); font-family: var(--font-ui); font-size: 0.85rem;">
                👤 ${user.first_name || user.username}
            </span>
            <button onclick="logout()"
                    style="margin-left: 16px; padding: 8px 16px;
                           background: transparent; color: var(--cream);
                           border: 2px solid var(--cream); border-radius: 2px;
                           font-family: var(--font-ui); font-size: 0.75rem;
                           letter-spacing: 1px; cursor: pointer;">
                ВЫЙТИ
            </button>
        `;
    } else {
        container.innerHTML = `
            <a href="/login/" class="nav-link">ВОЙТИ</a>
            <a href="/register/"
               style="margin-left: 16px; padding: 8px 16px;
                      background: var(--gold); color: var(--brown);
                      border-radius: 2px; font-family: var(--font-ui);
                      font-size: 0.75rem; letter-spacing: 1px;">
                РЕГИСТРАЦИЯ
            </a>
        `;
    }
}

function logout() {
    clearTokens();
    window.location.href = '/login/';
}

// ============================================
// СТРАНИЦА РЕГИСТРАЦИИ
// ============================================
function initRegisterPage() {
    const form = document.getElementById('register-form');
    const errorDiv = document.getElementById('register-error');
    const submitBtn = document.getElementById('submit-btn');

    // Обработка выбора роли
    document.querySelectorAll('.role-card').forEach(card => {
        card.addEventListener('click', () => {
            document.querySelectorAll('.role-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            card.querySelector('input').checked = true;
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Очищаем ошибки
        errorDiv.classList.add('hidden');
        document.querySelectorAll('.field-error').forEach(el => el.textContent = '');

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Проверка паролей
        if (data.password !== data.password2) {
            errorDiv.textContent = '⚠️ Пароли не совпадают';
            errorDiv.classList.remove('hidden');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'СОЗДАНИЕ...';

        try {
            const result = await apiFetch('/auth/register/', {
                method: 'POST',
                body: JSON.stringify(data),
            });

            setTokens(result.access, result.refresh);
            setUser(result.user);

            window.location.href = '/catalog/';
        } catch (error) {
            const errors = error.response?.data || {};

            // Показываем ошибки по полям
            let hasFieldErrors = false;
            Object.entries(errors).forEach(([field, messages]) => {
                const errorSpan = document.querySelector(`.field-error[data-field="${field}"]`);
                if (errorSpan) {
                    errorSpan.textContent = Array.isArray(messages) ? messages[0] : messages;
                    hasFieldErrors = true;
                }
            });

            // Общая ошибка
            if (!hasFieldErrors) {
                errorDiv.textContent = '⚠️ Ошибка регистрации. Проверьте данные.';
                errorDiv.classList.remove('hidden');
            }
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'ПОЛУЧИТЬ БИЛЕТ';
        }
    });
}

// ============================================
// СТРАНИЦА ВХОДА
// ============================================
function initLoginPage() {
    const form = document.getElementById('login-form');
    const errorDiv = document.getElementById('login-error');
    const submitBtn = document.getElementById('submit-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorDiv.classList.add('hidden');

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        submitBtn.disabled = true;
        submitBtn.textContent = 'ПРОВЕРКА...';

        try {
            const result = await apiFetch('/auth/login/', {
                method: 'POST',
                body: JSON.stringify(data),
            });

            setTokens(result.access, result.refresh);
            setUser(result.user);

            window.location.href = '/catalog/';
        } catch (error) {
            const errData = error.response?.data || {};
            const message = errData.detail
                || (typeof errData === 'object' ? Object.values(errData)[0]?.[0] : null)
                || 'Неверный логин или пароль';

            errorDiv.textContent = '⚠️ ' + (Array.isArray(message) ? message[0] : message);
            errorDiv.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'ВОЙТИ';
        }
    });
}

// ============================================
// СТРАНИЦА КАТАЛОГА
// ============================================
function initCatalogPage() {
    const container = document.getElementById('books-container');
    const searchInput = document.getElementById('search-input');
    const genreSelect = document.getElementById('genre-select');
    const resetBtn = document.getElementById('reset-btn');
    const countEl = document.getElementById('books-count');

    let searchTimeout;

    async function loadBooks() {
        container.innerHTML = `
            <div class="loading-state">
                <div class="loading-emoji">📚</div>
                <p>Открываем каталог...</p>
            </div>
        `;

        const params = new URLSearchParams();
        if (searchInput.value) params.append('search', searchInput.value);
        if (genreSelect.value) params.append('genre', genreSelect.value);

        try {
            const data = await apiFetch(`/books/?${params.toString()}`);
            const books = data.results || data;

            countEl.textContent = `${books.length} ${books.length === 1 ? 'издание' : 'изданий'} в нашей коллекции`;
            renderBooks(books);
        } catch (error) {
            container.innerHTML = `
                <div class="loading-state">
                    <div class="loading-emoji">⚠️</div>
                    <p>Ошибка загрузки каталога</p>
                </div>
            `;
        }
    }

    function renderBooks(books) {
        if (books.length === 0) {
            container.innerHTML = `
                <div class="loading-state">
                    <div class="loading-emoji">🔍</div>
                    <p>Ничего не найдено</p>
                </div>
            `;
            return;
        }

        container.innerHTML = books.map(book => {
            const isAvailable = book.available_copies > 0;
            const emoji = {
                'fiction': '📕',
                'science': '📗',
                'history': '📘',
                'biography': '📙',
                'fantasy': '📓',
            }[book.genre] || '📖';

            const authors = book.authors?.map(a => a.name).join(', ') || 'Неизвестный автор';

            return `
                <div class="book-card">
                    <div class="book-cover">
                        ${emoji}
                        <span class="book-availability ${isAvailable ? 'available' : 'unavailable'}">
                            ${isAvailable ? `✓ ${book.available_copies}` : '✗ Нет'}
                        </span>
                    </div>
                    <h3 class="book-title">${book.title}</h3>
                    <p class="book-author">${authors}</p>
                    <div class="book-info">
                        <span>${book.genre}</span>
                        <span>📚 ${book.total_copies} экз.</span>
                    </div>
                    <button class="book-borrow-btn"
                            ${!isAvailable ? 'disabled' : ''}
                            onclick="borrowBook(${book.id}, '${book.title.replace(/'/g, "\\'")}')">
                        ${isAvailable ? 'ВЗЯТЬ КНИГУ' : 'НЕДОСТУПНА'}
                    </button>
                </div>
            `;
        }).join('');
    }

    // Поиск с задержкой
    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(loadBooks, 400);
    });

    genreSelect.addEventListener('change', loadBooks);

    resetBtn.addEventListener('click', () => {
        searchInput.value = '';
        genreSelect.value = '';
        loadBooks();
    });

    loadBooks();
}

// ---------- Взять книгу ----------
async function borrowBook(bookId, bookTitle) {
    const user = getUser();
    if (!user) {
        alert('Войдите в систему, чтобы взять книгу');
        window.location.href = '/login/';
        return;
    }

    // Срок возврата — через 14 дней
    const dueDate = new Date();
    dueDate.setDate(dueDate.getDate() + 14);
    const dueDateStr = dueDate.toISOString().split('T')[0];

    try {
        await apiFetch('/loans/', {
            method: 'POST',
            body: JSON.stringify({
                book: bookId,
                due_date: dueDateStr,
            }),
        });

        alert(`Книга "${bookTitle}" успешно взята!\nВернуть до: ${dueDateStr}`);
        location.reload();
    } catch (error) {
        const errData = error.response?.data || {};
        alert('Ошибка: ' + JSON.stringify(errData, null, 2));
    }
}

// ============================================
// ИНИЦИАЛИЗАЦИЯ
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    updateAuthNav();
});
