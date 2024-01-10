let musicList = [];

function addMusic() {
    const title = document.getElementById('title').value;
    const artist = document.getElementById('artist').value;
    const genre = document.getElementById('genre').value;
    const lyrics = document.getElementById('lyrics').value;
    const releaseYear = document.getElementById('releaseYear').value;

    // 음악 카드 생성
    const musicCard = document.createElement('div');
    musicCard.className = 'music-card';
    musicCard.innerHTML = `
        <h2>제목: ${title}</h2>
        <p>가수: ${artist}</p>
        <p>장르: ${genre}</p>
        <p>가사: ${lyrics}</p>
        <p>발매 연도: ${releaseYear}</p>
    `;

    const deleteButton = document.createElement('span');
    deleteButton.innerHTML = '삭제';
    deleteButton.className = 'delete-button';
    deleteButton.addEventListener('click', function () {
        // 사용자에게 확인을 받는 알림창
        const confirmDelete = confirm('삭제하시겠습니까?');

        // 확인을 눌렀을 때만 삭제 동작 실행
        if (confirmDelete) {
            deleteMusic(musicCard);
        }
    });
    // 음악 카드에 삭제 버튼 추가
    musicCard.appendChild(deleteButton);

    // 음악 목록에 음악 카드 추가
    document.getElementById('musicList').appendChild(musicCard);

    // 음악 목록 배열에 음악 정보 추가
    musicList.push({
        title: title,
        artist: artist,
        genre: genre,
        lyrics: lyrics,
        releaseYear: releaseYear
    });

    // 음악 추가 후 폼 초기화
    document.getElementById('musicForm2').reset();

    // 음악 목록을 로컬 스토리지에 저장
    saveMusicListToLocalStorage();

    alert('음악을 추가하였습니다.');
}

// 음악 삭제 함수
function deleteMusic(musicCard) {
    // 음악 목록 배열에서 해당 음악 정보 제거
    const title = musicCard.querySelector('h2').textContent.split('제목: ')[1];
    musicList = musicList.filter(music => music.title !== title);

    // 음악 목록에서 음악 카드 제거
    musicCard.remove();

    // 음악 목록을 로컬 스토리지에 저장
    saveMusicListToLocalStorage();
}

// 페이지 로드 시 음악 목록을 로컬 스토리지에서 불러와서 표시
function loadMusicListFromLocalStorage() {
    const savedMusicList = localStorage.getItem('musicList');
    if (savedMusicList) {
        musicList = JSON.parse(savedMusicList);

        // 저장된 음악 목록을 화면에 표시
        const musicListContainer = document.getElementById('musicList');
        musicList.forEach(music => {
            const musicCard = document.createElement('div');
            musicCard.className = 'music-card';
            musicCard.innerHTML = `
                <h2>제목: ${music.title}</h2>
                <p>가수: ${music.artist}</p>
                <p>장르: ${music.genre}</p>
                <p>가사: ${music.lyrics}</p>
                <p>발매 연도: ${music.releaseYear}</p>
            `;

            const deleteButton = document.createElement('span');
            deleteButton.innerHTML = '삭제';
            deleteButton.className = 'delete-button';
            deleteButton.addEventListener('click', function () {
                // 사용자에게 확인을 받는 알림창
                const confirmDelete = confirm('삭제하시겠습니까?');

                // 확인을 눌렀을 때만 삭제 동작 실행
                if (confirmDelete) {
                    deleteMusic(musicCard);
                }
            });

            // 음악 카드에 삭제 버튼 추가
            musicCard.appendChild(deleteButton);

            // 음악 목록에 음악 카드 추가
            musicListContainer.appendChild(musicCard);
        });
    }
}

// 페이지 로드 시 음악 목록을 로컬 스토리지에서 불러옴
loadMusicListFromLocalStorage();

// 로컬 스토리지에 음악 목록 저장
function saveMusicListToLocalStorage() {
    localStorage.setItem('musicList', JSON.stringify(musicList));
}