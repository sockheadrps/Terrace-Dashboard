<script>
    import { state } from "../../stores";

    let services = []

    $: {
        state.subscribe(value => {
            try {
                if (value['serviceList']){
                    services = value['serviceList']
                }
            }
            catch (error) {
                console.log(error)
            }
        });
    }

</script>

<div class="service-area">
    {#each services as service}
        <div class=service>{service}</div>
    {/each}
</div>

<style>

.service-area {
    display: flex;
    align-items: center;
    background: linear-gradient(to right bottom, rgba(10, 6, 24, 0.75), rgba(10, 6, 24, 0.69));
    border-radius: 2rem;
    justify-content: center;
    min-height: 5rem;
    user-select: none;
    margin-left: 2rem;
    margin-right: 2rem;
}

.service{
    display: flex;
    flex-direction: column;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    color: #808080;

    box-sizing: border-box;
    border: 1px solid rgba(10, 6, 24, 0.021);
    background:rgba(87, 87, 99, 0.1);
    border-radius: 2rem;
    backdrop-filter: blur(1.1rem);
    margin: .5rem;
    padding: .5rem;
    text-align: center;
    cursor: pointer;
    transition: all .2s ease-out;
}

.service:hover {
  background: linear-gradient(rgba(10, 6, 24, 0.904),rgba(10, 6, 24, 0.877)) padding-box,
              linear-gradient(to right, rgba(50, 2, 94, 0.774), rgb(26, 28, 143)) border-box;
  border-radius: 2rem;
  border: 1px solid transparent;
  opacity: .7;
    color: #525151;
}

</style>