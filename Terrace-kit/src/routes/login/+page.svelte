

<script lang="ts">
  import * as Threlte from '@threlte/core'
  import * as Three from 'three'
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
  import { gsap } from 'gsap'
  const gltfloader = new GLTFLoader()
  import { onMount } from 'svelte'
  let ready = false

  onMount(() => {
    // Canvas
    const canvas = document.querySelector('canvas.webgl')
    // Scene
    const scene = new Three.Scene()

    //tablet
    let tl = gsap.timeline()
    gltfloader.load('/static/tab.gltf', (gltf) => {
      scene.add(gltf.scene)

      // initial scale of model
      gltf.scene.scale.set(0.9, 0.9, 0.9)

      // lays the model back a bit
      gltf.scene.rotation.set(0, 3.3, .2)	
      
      // Scales the model down (this makes it appear a little like its moving away from the user as well, but its just scaling down)
        tl.to(gltf.scene.scale, {x: 0.2, y: 0.2, z: 0.2, duration: 1})

      // Rotation
        tl.to(gltf.scene.rotation, {y: 4.0, duration: .5, ease: "SlowMo.ease.config(0.7, 0.7, false"})

      // Translation
        tl.to(gltf.scene.position, {x: 1.1,  duration: .9, ease: "Power4.easeInOut"})
      ready = true;      
    })

    // Lights

    const pointLight = new Three.AmbientLight(0xffffff, 4.5)
    pointLight.position.x = 4
    pointLight.position.y = 3
    pointLight.position.z = 4
    scene.add(pointLight)

    /**
     * Sizes
     */
    const sizes = {
      width: window.innerWidth,
      height: window.innerHeight,
    }

    window.addEventListener('resize', () => {
      // Update sizes
      sizes.width = window.innerWidth
      sizes.height = window.innerHeight

      // Update camera
      camera.aspect = sizes.width / sizes.height
      camera.updateProjectionMatrix()

      // Update renderer
      renderer.setSize(sizes.width, sizes.height)
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    })

    /**
     * Camera
     */
    // Base camera
    const camera = new Three.PerspectiveCamera(
      75,
      sizes.width / sizes.height,
      0.1,
      100
    )
    camera.position.x = 0
    camera.position.y = 0
    camera.position.z = 2
    scene.add(camera)

    // Controls
    // const controls = new OrbitControls(camera, canvas)
    // controls.enableDamping = true

    /**
     * Renderer
     */
    const renderer = new Three.WebGLRenderer({
      canvas: canvas,
      alpha: true,
    })
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

    /**
     * Animate
     */

    const clock = new Three.Clock()

    const tick = () => {
      const elapsedTime = clock.getElapsedTime()

      // Render
      renderer.render(scene, camera)

      // Call tick again on the next frame
      window.requestAnimationFrame(tick)
    }

    tick()

    });

</script>
<body class="h-100 bg-stone-900">
  <canvas class="webgl"></canvas>
    <div class="bg-img h-100">
        <!-- container -->
        <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 text-center px-7 py-14 w-96 bg-white bg-opacity-5 shadow-md">
          <form action="#">
            <!-- user -->
            <div class=" relative h-11 w-full flex bg-white bg-opacity-95 text-left
                         hover:opacity-80 transition duration-300 ease-in-out">
              <span class="text-gray-400 w-10 leading-10"></span>
              <input class="h-full w-full bg-transparent border-none outline-none text-gray-400 text-sm" type="text" required placeholder="Email">
            </div>
            <!-- password -->
            <div class="mt-4 relative h-11 w-full flex bg-white bg-opacity-95
                        hover:opacity-80 transition duration-300 ease-in-out">
              <span class="text-gray-400 w-10 leading-10"></span>
              <input class="h-full w-full bg-transparent border-none outline-none text-gray-400 text-sm" type="password" required placeholder="Password">
            </div>
            <!-- forgot password -->
            <div class="my-2 text-left  my-0">
              <a class=" text-slate-500" href="#">Forgot Password?</a>
            </div>
            <!-- submit-->
              <input class="w-full py-2 bg-blue-500 border-2 border-blue-600 text-white text-lg space-x-7 font-bold cursor-pointer hover:bg-blue-600 transition duration-300 ease-in-out" type="submit" value="LOGIN">
            <!-- no account -->
            <div class="mt-10">
                <div class="text-white">Don't have account?
                    <a class="text-blue-400" href="#">Signup Now</a>
                </div>
                <!-- signup -->
                <div class="text-white">Or
                    <a class="text-blue-400"  href="#">Continue as guest</a>
                </div>
            </div>
          </form>
        </div>
      </div>

</body>

<style>
*
{
    margin: 0;
    padding: 0;
}

body
{
    height: 100vh;
    font-family: 'Poppins';
    background: rgb(55, 62, 70);
}

.webgl
{
    position: fixed;
    top: 0;
    left: 0;
    outline: none;
}



@import url('https://fonts.googleapis.com/css?family=Montserrat:400,500,600,700|Poppins:400,500&display=swap');
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  user-select: none;
}

.bg-img:after{
  position: absolute;
  content: '';
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: rgba(0,0,0,0.7);
}
</style>