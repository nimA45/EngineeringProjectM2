<script>
    import AdminDashboard from '../../components/admin-dashboard.svelte';
    import { adminConnected } from '../../store/admin-store';
    
    let password = null

    async function submitForm() {
        await fetch('http://localhost:5000/api/admin', {
            method: 'POST',
            headers: new Headers({
                "Content-Type" : "application/json"
            }),
            body: JSON.stringify({
                password
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

            $adminConnected = res
        })
        .catch((err) => alert(err))
    }
</script>

<main class="container">
    {#if $adminConnected}
        <AdminDashboard />
    {:else}
        <div class="form-container">
            <form on:submit|preventDefault={submitForm}>
                <h2>Admin Dashboard</h2>
                <input bind:value={password} type="password" placeholder="Admin password">
                <button type="submit">Connect</button>
            </form>
        </div>
    {/if}
   
</main>

<style>
    .container {
        margin: 40px 20vw
    }

    .form-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    form {
        width: 40vw;
    }
</style>