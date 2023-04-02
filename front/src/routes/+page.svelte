<script>
    import { goto } from '$app/navigation';
    import { userConnected } from '../store/user-store'

    let sessionId = null
    let sessionName = null

    let loading = false

    async function submitForm() {
        loading = true

        console.log(sessionId)
        console.log(sessionName)

        return await fetch('http://localhost:5000/api/session', {
            method: 'POST',
            headers: new Headers({
                "Content-Type" : "application/json"
            }),
            body: JSON.stringify({
                id: sessionId,
                name: sessionName
            })
        })
        .then((res) => res.json())
        .then((res) => {
            if(res.error) {
                throw res.error
            }

            if(res.detail) {
                throw res.detail[0].msg
            }

            console.log(res)
            $userConnected = res
            loading = false
        })
        .catch((err) => {
            loading = false
            alert(err)
        })
    }

    $: {
        if($userConnected)
            goto(`/quizz/${$userConnected.session_id}`)
    }
</script>





<!-- Main -->
<main class="container">
    <article class="grid">
      <div>
        <hgroup>
          <h1>ACCESS TALENT</h1>
          <h2>Sign in</h2>
        </hgroup>
        <form on:submit|preventDefault={submitForm}> 
          <input bind:value={sessionName} type="text" name="name" placeholder="Name" aria-label="Name" autocomplete="nickname" required>
          <input bind:value={sessionId} type="password" name="password" placeholder="Session-ID" aria-label="Password" autocomplete="current-password" required>
          <fieldset>
            <label for="remember">
              <input type="checkbox" role="switch" id="remember" name="remember">
              Remember me
            </label>
          </fieldset>
          <button type="submit" class="contrast" aria-busy={loading}>Login</button>
        </form>
      </div>
      <div></div>
    </article>
  </main><!-- ./ Main -->


<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-shrink: 0;
        height: 100vh;
    }

    form {
        width: 40vw;
    }
</style>
