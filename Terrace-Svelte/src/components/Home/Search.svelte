<div class="search__area">
    <div class="search__bar">
        <img src="assets/g-svg.svg" width="35" height="35" class="i-svg g-svg" alt=""/>
        <form action="https://www.google.com/search" method="get" id="search-form">
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

.search__bar img {
    float: left;
    width: 5%;
    margin-top: 5px;
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
</style>
