<script lang="ts">
    import { state } from "$lib/stores";
    let services: string[] = [];

    $: {
        try {
            if ($state['serviceList']){
                services = $state['serviceList'];
            }
        } catch (error) {
            console.log(error)
        }
    }
</script>

<div class="service-area">
    {#each services as service}
        <div class={service}>{service}</div>
    {/each}
</div>

<style>

.service-area {
    display: flex;
    align-items: center;
    background: linear-gradient(
        to left top,
         rgba(24, 24, 24, 0.822),
         rgba(15, 15, 15, 0.863)
         );
    border-radius: 2rem;
    justify-content: center;
    min-height: 5rem;
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
    background: linear-gradient(rgb(15, 15, 15),rgb(39, 39, 39)) padding-box,
                linear-gradient(to right, rgba(84, 69, 99, 0.034), rgba(101, 101, 143, 0)) border-box;
    border-radius: 2rem;
    border: 1px solid transparent;
    opacity: .7;
    color: #525151;
}

</style>
