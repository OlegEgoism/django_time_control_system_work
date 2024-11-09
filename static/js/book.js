function incrementDownload(bookId) {
    // Асинхронный запрос для увеличения счетчика загрузок
    fetch(`/book_download_count/${bookId}/`)
        .then(response => response.json())
        .then(data => {
            const downloadCountElement = document.querySelector(`#downloads-${bookId}`);
            if (downloadCountElement) {
                downloadCountElement.innerText = `Скачал(и): ${data.new_count}`;
            }
            // После обновления счетчика инициируем скачивание файла
            window.location.href = `/book_download_file/${bookId}/`;
        })
        .catch(error => console.error('Ошибка при обновлении счетчика:', error));
}
