let repeat = 0;

function timer() {
  const song = document.querySelector(".song");
  const play = document.querySelector(".play");
  const reset = document.querySelector(".reset");
  const pausebtn = document.querySelector(".pause");
  const click = document.querySelector(".click");

  // Time display
  const minuteDisplay = document.querySelector(".minute");
  const secondDisplay = document.querySelector(".second");

  // Links
  const link1 = document.querySelector(".shortLink");
  const link2 = document.querySelector(".longLink");

  //Duration
  // const formDuration = document.getElementById("duration").value;
  const formDuration = workDuration;
  let duration = formDuration * 60;

  let displayMinutes = ("0" + Math.floor(duration / 60)).slice(-2);
  let displaySeconds = ("0" + Math.floor(duration % 60)).slice(-2);

  for (const mdisplay in minuteDisplay) {
    mdisplay.textContent = `${displayMinutes}`;
  }

  for (const sdisplay in secondDisplay) {
    sdisplay.textContent = `${displaySeconds}`;
  }

  play.addEventListener("click", () => {
    click.play();
    song.play();
    pausebtn.style.display = "flex";
    play.style.display = "none";
  });

  pausebtn.addEventListener("click", () => {
    click.play();
    song.pause();
    pausebtn.style.display = "none";
    play.style.display = "flex";
  });

  song.ontimeupdate = () => {
    let currentTime = song.currentTime;
    let elapsed = duration - currentTime;
    let seconds = Math.floor(elapsed % 60);
    let minutes = Math.floor(elapsed / 60);

    // Edit time display
    let formatMinutes = ("0" + minutes).slice(-2);
    let formatSeconds = ("0" + seconds).slice(-2);
    minuteDisplay.textContent = `${formatMinutes}`;
    secondDisplay.textContent = `${formatSeconds}`;

    [link1, link2, reset].forEach((element) => {
      element.addEventListener("click", () => {
        click.play();
        song.pause();
        song.currentTime = 0;
        pausebtn.style.display = "none";
        play.style.display = "flex";
        if (reset.classList.contains("btn-active")) return;
        reset.classList.add("btn-active");
        // remove class after 2 seconds
        setTimeout(() => {
          reset.classList.remove("btn-active");
        }, 150);
      });
    });

    if (currentTime >= duration) {
      click.play();
      song.pause();
      song.currentTime = 0;
      pausebtn.style.display = "none";
      play.style.display = "flex";
      repeat = repeat + 1;
      console.log(repeat);

      if (repeat > 3) {
        pages("long-break", "work", "short-break");
        repeat = 0;
      } else {
        pages("short-break", "work", "long-break");
      }
    }
  };
}

timer();

function shortTimer() {
  const song = document.querySelector(".shortSong");
  const play = document.querySelector(".shortPlay");
  const reset = document.querySelector(".shortReset");
  const pausebtn = document.querySelector(".shortPause");
  const click = document.querySelector(".click");

  // Time display
  const minuteDisplay = document.querySelector(".shortMinute");
  const secondDisplay = document.querySelector(".shortSecond");

  // Links
  const link1 = document.querySelector(".workLink");
  const link2 = document.querySelector(".longLink");

  //Duration
  // const formDuration = document.getElementById("duration").value;
  const formDuration = shortDuration;
  let duration = formDuration * 60;

  let displayMinutes = ("0" + Math.floor(duration / 60)).slice(-2);
  let displaySeconds = ("0" + Math.floor(duration % 60)).slice(-2);

  for (const mdisplay in minuteDisplay) {
    mdisplay.textContent = `${displayMinutes}`;
  }

  for (const sdisplay in secondDisplay) {
    sdisplay.textContent = `${displaySeconds}`;
  }

  play.addEventListener("click", () => {
    click.play();
    song.play();
    pausebtn.style.display = "flex";
    play.style.display = "none";
  });

  pausebtn.addEventListener("click", () => {
    click.play();
    song.pause();
    pausebtn.style.display = "none";
    play.style.display = "flex";
  });

  song.ontimeupdate = () => {
    let currentTime = song.currentTime;
    let elapsed = duration - currentTime;
    let seconds = Math.floor(elapsed % 60);
    let minutes = Math.floor(elapsed / 60);

    // Edit time display
    let formatMinutes = ("0" + minutes).slice(-2);
    let formatSeconds = ("0" + seconds).slice(-2);
    minuteDisplay.textContent = `${formatMinutes}`;
    secondDisplay.textContent = `${formatSeconds}`;

    [link1, link2, reset].forEach((element) => {
      element.addEventListener("click", () => {
        click.play();
        song.pause();
        song.currentTime = 0;
        pausebtn.style.display = "none";
        play.style.display = "flex";
        if (reset.classList.contains("btn-active")) return;
        reset.classList.add("btn-active");
        // remove class after 2 seconds
        setTimeout(() => {
          reset.classList.remove("btn-active");
        }, 150);
      });
    });

    if (currentTime >= duration) {
      click.play();
      song.pause();
      song.currentTime = 0;
      pausebtn.style.display = "none";
      play.style.display = "flex";
      pages("work", "short-break", "long-break");
    }
  };
}

shortTimer();

function longTimer() {
  const song = document.querySelector(".longSong");
  const play = document.querySelector(".longPlay");
  const reset = document.querySelector(".longReset");
  const pausebtn = document.querySelector(".longPause");
  const click = document.querySelector(".click");

  // Time display
  const minuteDisplay = document.querySelector(".longMinute");
  const secondDisplay = document.querySelector(".longSecond");

  // Links
  const link1 = document.querySelector(".workLink");
  const link2 = document.querySelector(".shortLink");

  //Duration
  const formDuration = longDuration;
  let duration = formDuration * 60;

  let displayMinutes = ("0" + Math.floor(duration / 60)).slice(-2);
  let displaySeconds = ("0" + Math.floor(duration % 60)).slice(-2);

  for (const mdisplay in minuteDisplay) {
    mdisplay.textContent = `${displayMinutes}`;
  }

  for (const sdisplay in secondDisplay) {
    sdisplay.textContent = `${displaySeconds}`;
  }

  play.addEventListener("click", () => {
    click.play();
    song.play();
    pausebtn.style.display = "flex";
    play.style.display = "none";
  });

  pausebtn.addEventListener("click", () => {
    click.play();
    song.pause();
    pausebtn.style.display = "none";
    play.style.display = "flex";
  });

  song.ontimeupdate = () => {
    let currentTime = song.currentTime;
    let elapsed = duration - currentTime;
    let seconds = Math.floor(elapsed % 60);
    let minutes = Math.floor(elapsed / 60);

    // Edit time display
    let formatMinutes = ("0" + minutes).slice(-2);
    let formatSeconds = ("0" + seconds).slice(-2);
    minuteDisplay.textContent = `${formatMinutes}`;
    secondDisplay.textContent = `${formatSeconds}`;

    [link1, link2, reset].forEach((element) => {
      element.addEventListener("click", () => {
        click.play();
        song.pause();
        song.currentTime = 0;
        pausebtn.style.display = "none";
        play.style.display = "flex";
        if (reset.classList.contains("btn-active")) return;
        reset.classList.add("btn-active");
        // remove class after 2 seconds
        setTimeout(() => {
          reset.classList.remove("btn-active");
        }, 150);
      });
    });

    if (currentTime >= duration) {
      click.play();
      song.pause();
      song.currentTime = 0;
      pausebtn.style.display = "none";
      play.style.display = "flex";
      pages("work", "short-break", "long-break");
    }
  };
}

longTimer();

function pages(shown, hidden1, hidden2) {
  document.getElementById(shown).style.display = "flex";
  document.getElementById(hidden1).style.display = "none";
  document.getElementById(hidden2).style.display = "none";
  return false;
}

pages("work", "short-break", "long-break");
