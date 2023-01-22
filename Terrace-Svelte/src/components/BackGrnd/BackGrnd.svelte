
<script>
    
</script>
<div class="bCirContainer">
    <div class="bigCir">
</div>
</div> 

<div class="center-1">
        <div class="small-1"></div>
</div>

<div class="center-2">
    <div class=" small-2"></div>
</div>
<style>

:root {
  --main-bg-color: brown;
  --cir-top: -580px;
  --cir-bot: 340px;
}

.bCirContainer{
    position: relative;
    z-index: --3;
}


.bigCir {
    width: 700px;
    height: 700px;
    position: fixed;
    top: 50%;
    left: 50%;
    margin-top: -350px;
    margin-bottom: -350px;
    background: linear-gradient(to right bottom, rgb(0, 0, 0), rgb(33, 36, 116));

    border-radius: 50%;
    box-shadow: 
        0px -30px 250px rgb(7, 9, 83),
        -30px 0px 250px rgba(11, 62, 121, 0.76),
        30px 0px 250px rgba(71, 26, 92, 0.692), 
        0px 30px 250px rgba(70, 9, 54, 0.692);
    transition: 1.8s;
    animation:bigCir 400s  linear infinite;
    animation:createBox 2s  linear infinite ease-in-out;

    z-index: -1;
    filter: blur(.2rem);
    

}
@keyframes bigCir {
    from {transform: rotate(0deg);}
    to {transform: rotate(0deg);}
}
@keyframes createBox {
  from {
    transform: scale(.5);
  }
  to {
    transform: scale(.99);
  }
}


.center-1{
    width: 40px;
    height: 40px;
    position: fixed;
    top: 50%;
    left: 50%;
    z-index: -2;
    animation:around1 120s  linear infinite;
}

@keyframes around1 {
    from {transform: rotate(0deg);}
    to {transform: rotate(-360deg);}
}


.center-3{
    width: 50px;
    height: 50px;
    position: fixed;
    top: 30%;
    left: 75%;
    margin-top: -25px;
    margin-left: -25px;
    z-index: -1;
    animation:around3 120s  linear infinite;
}
@keyframes around3 {
    from {transform: rotate(240deg);}
    to {transform: rotate(-120deg);}
}

.small-1{
    width: 40px;
    height: 140px;
    position: fixed;
    top: 330px;
    left: 330px;
    margin-top: -165px;
    margin-left: -165px;
    background: rgba(10, 6, 24, 0.356);
    scale: .6;
    border-radius: 50%;
    z-index: 3;
    box-shadow: 
    0px -15px 100px rgb(0, 52, 165),
    -15px 0px 100px rgba(71, 0, 153, 0.493),
    15px 0px 100px rgb(55, 0, 107), 
    0px 15px 100px rgba(88, 0, 0, 0.37);
    filter: blur(.1rem);
    animation: pulse infinite 180s ease-in-out;
}






.small-2{
    width: 250px;
    height: 240px;
    position: fixed;
    top: 400px;
    left: 250px;
    margin-top: -165px;
    margin-left: -165px;
    background: rgba(10, 6, 24, 0.226);
    scale: .6;
    border-radius: 50%;
    z-index: -3;
    box-shadow: 
    0px -15px 100px rgb(0, 52, 165),
    -15px 0px 100px rgba(71, 0, 153, 0.493),
    15px 0px 100px rgb(55, 0, 107), 
    0px 15px 100px rgba(88, 0, 0, 0.37);
    animation: around5 infinite 180s ease-in-out;
    filter: blur(.6rem);


}
@keyframes around5 {
    from {transform: rotate(240deg);}
    to {transform: rotate(-120deg);}
}

.small-3{
    width: 40px;
    height: 140px;
    position: fixed;
    top: 330px;
    left: 330px;
    margin-top: -165px;
    margin-left: -165px;
    background: rgba(0, 8, 31, 0.068);
    scale: .6;
    border-radius: 50%;
    z-index: 3;
    box-shadow: 
    0px -125px 100px rgb(0, 90, 163),
    -125px 0px 100px rgb(0, 114, 190),
    125px 0px 100px rgb(101, 0, 160), 
    0px 125px 100px rgb(1, 52, 119);
    animation: pulse infinite 180s ease-in-out;
    filter: blur(.1rem);
}

@keyframes pulse {
    from {transform: rotate(0deg);}
    to {transform: rotate(-360deg);}
}

</style>

