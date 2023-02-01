<script>
    const actions = ["https://www.google.com/search", "https://www.youtube.com/results?search_query="]
    let clicked = "",
        action  = 0;

    function onclick() {
        clicked = clicked ? "" : "clicked";
        action = action ? 0 : 1;
    }
</script>


<div class="search__area">
    <div class="flip-container" on:click={onclick} on:keydown={onclick}>
        <div class="card {clicked}">
            <div class="front">
                <img src="/assets/g-svg.svg" width="35" height="35" class="i-svg g-svg" alt="google icon"/> 
            </div>
            <div class="back">
                <img src="/assets/youtube-icon.svg" width="35" height="35" class="i-svg yt-svg" alt="youtube icon"/> 
            </div>
        </div>
    </div>
    <div class="search__bar">
        <form action="{actions[action]}" method="get" id="search-form">
            <input type="text" class="search" placeholder="Search...." name="q">
        </form>
    </div>
</div>


<style>
.search__area {
    display: grid;
    grid-template-columns: 1fr;
    margin-left: 2rem;
    margin-right: 2rem;
    background: linear-gradient(
        to left top,
         rgba(24, 24, 24, 0.822),
         rgba(15, 15, 15, 0.863)
         );
    border-radius: 1.2em;
    padding: .5rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.search__bar form{
    display: inline-block;
    width: 90%;
    background-color: rgba(39, 39, 39, 0.164);
    border-radius: 1.2em;
    margin: auto;
}

input {
    text-align: center;
    border: 0;
    background-color: transparent;
    color: rgb(243, 255, 240);
    width: 100%;
    padding: auto;
    height: 100%;
    margin-top: 10px;
}

.search__bar input:focus {
    outline: 0;
}

.flip-container{
    position: relative;
    float: left;
    width: 5%;
    height: 100%;
    margin-bottom: 8px;
}

.card {
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: all 0.5s;
    border-radius: 50%;
}

.card:hover {
    transform: scale(1.2);
}

.front {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
}

.back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  transform: rotateY(180deg);
}

.clicked {
    transform: rotateY(180deg);
}

.clicked:hover {
    transform: rotateY(180deg);
}

</style>
