<script>
    import { onMount } from 'svelte';
    import { adminConnected } from '../store/admin-store';

    let quizzes = [];
    let selectedName = '';
    let selectedQuizz = null;

    onMount(() => {
        getQuizz();
    });

    async function getQuizz() {
        quizzes = await fetch('http://localhost:5000/api/admin/quizz', {
            headers: new Headers({
                "Authorization" : $adminConnected
            })
        })
        .then((res) => res.json())
        .then((res) => {
            if(res?.detail) {
                throw res.detail[0].msg;
            }

            return res;
        });
    }

    let job = null;
    let experience = null;
    let name = null;

    async function submitForm(e) {
        e.preventDefault();
        e.target[0].setAttribute('disabled', "true");
        e.target[1].setAttribute('disabled', "true");
        e.target[2].setAttribute('disabled', "true");
        e.target[3].setAttribute('aria-busy', "true");

        await fetch('http://localhost:5000/api/admin/quizz', {
            method: 'POST',
            headers: new Headers({
                "Content-Type" : "application/json",
                "Authorization" : $adminConnected
            }),
            body: JSON.stringify({
                job,
                experience,
                name
            })
        })
        .then(async res => {
            await getQuizz();
        })
        .catch((err) => {alert(err)});

        e.target[0].removeAttribute('disabled');
        job = null;

        e.target[1].removeAttribute('disabled');
        experience = null;

        e.target[2].removeAttribute('disabled');
        name = null;

        e.target[3].setAttribute('aria-busy', "false");
    }

    function selectName(e) {
        selectedName = e.target.value;
        selectedQuizz = quizzes.find(quizz => quizz.name === selectedName);
    }

</script>

<section>
    <form on:submit={submitForm}>
        <input type="text" bind:value={job} placeholder="job" required>
        <input type="number" bind:value={experience} placeholder="years of experience" required>
        <input type="text" bind:value={name} placeholder="username" required>
        <button type="submit">Create a quiz</button>
    </form>
</section>
<section>
    <select on:change={selectName}>
        <option value="" disabled selected hidden>Choose a name</option>
        {#each quizzes as quizz}
            <option value={quizz.name}>{quizz.name}</option>
        {/each}
    </select>
    {#if selectedQuizz === null}
        <p>No quizz selected</p>
    {:else}
        <article>
            <header>
                <p><mark>Session ID :</mark> {selectedQuizz.id}</p>
                <p><mark>Name :</mark> {selectedQuizz.name}</p>
                <p><mark>Job :</mark> {selectedQuizz.job}</p>
                <p><mark>Experience :</mark> {selectedQuizz.experience}</p>
            </header>

            {#each selectedQuizz.questions as question}
                <section>
                    <p><mark>Question :</mark> {question.question}</p>
                    <p><mark>User answer :</mark> {question.user_answer}</p>
                    <p><mark>Chat response :</mark> {question.chat_response}</p>
                </section>

                {#if question.keyword_questions.length > 0}
                    <div class="keyword_questions">
                        <h3>Keyword questions</h3>
                        {#each question.keyword_questions as keyword_question (keyword_question.id)}
                            <div class="keyword_question">
                                <p><mark>Question :</mark> {keyword_question.question}</p>
                                <p><mark>User answer :</mark> {keyword_question.user_answer}</p>
                                <p><mark>Chat response :</mark> {keyword_question.chat_response}</p>
                            </div>
                        {/each}
                    </div>
                {/if}   
            {/each}
        </article>
    {/if}
</section>

<style>
    .container {
        padding: 40px 20vw
    }

    .keyword_question:nth-child(even) { 
        background: #1b2e3c;    
    }
</style>