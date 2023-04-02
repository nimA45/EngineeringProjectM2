<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { userConnected } from "../../../store/user-store";

    let quizz = null

    onMount(() => {
        getQuizz()    
    })

	async function getQuizz() {
        try {
            quizz = await fetch('http://localhost:5000/api/quizz', {
                headers: new Headers({
                    Authorization: $userConnected.token
                })
            })
            .then(res => res.json())
            .then((res) => {
                if(res.error) {
                    throw res.error
                }

                if(res.detail) {
                    throw res.detail[0].msg
                }
                console.log(res)

                return res
            })
            .catch((err) => {
                alert(err)
                goto('/')
            })
        } catch (err) {
            goto('/')
        }
    }

    async function submitAnswer(e) {
        e.target[0].setAttribute("disabled", "true");
        e.target[1].setAttribute("aria-busy", "true");

        const question_id = e.target.id
        const content = e.target[0].value

        await fetch(`http://localhost:5000/api/quizz/${$userConnected.session_id}/${question_id}`,{
            method: 'POST',
            headers: new Headers({
                Authorization: $userConnected.token,
                "Content-Type" : "application/json"
            }),
            body: JSON.stringify({
                content
            })
        })
        .then((res) => res.json())
        .then((res) => {
            quizz.questions = quizz.questions.map((question) => {
                
                if(question.id != question_id)
                    return question

                return res
            }) 
            quizz = quizz
        })
        .catch((err) => {
            alert(err)
        })

        e.target[0].removeAttribute("disabled");
        e.target[1].setAttribute("aria-busy", "false");
    }

    async function submitKeywordAnswer(e) {
        e.target[0].setAttribute("disabled", "true");
        e.target[1].setAttribute("aria-busy", "true");

        const question_id = e.target[1].value
        const keyword_question_id = e.target.id
        const content = e.target[0].value


        await fetch(`http://localhost:5000/api/quizz/${$userConnected.session_id}/${question_id}/${keyword_question_id}`,{
            method: 'POST',
            headers: new Headers({
                Authorization: $userConnected.token,
                "Content-Type" : "application/json"
            }),
            body: JSON.stringify({
                content
            })
        })
        .then((res) => res.json())
        .then((res) => {
            quizz.questions = quizz.questions.map((question) => {
                
                if(question.id != question_id)
                    return question

                return res
            }) 
            quizz = quizz
        })
        .catch((err) => {
            alert(err)
        })

        e.target[0].removeAttribute("disabled");
        e.target[1].setAttribute("aria-busy", "false");
    }


</script>
<div class="container">
    {#if !(quizz)}
        <div aria-busy="true">Chargement</div>
    {:else}
        <article>
            <header>
                <p><mark>Session ID :</mark> {quizz.id}</p>
                <p><mark>Name :</mark> {quizz.name}</p>
            </header> 
            <p><mark>Job :</mark> {quizz.job}</p>
            <p><mark>Experience :</mark> {quizz.experience} year{#if quizz.experience > 2}s{/if}</p>
        </article>

        {#each quizz.questions as question (question.id)}
            <article>
                <header>
                    <h2>Question {question.id + 1}</h2>
                </header>
                <section>
                    <div class="questions">
                        <p><mark>Question :</mark> {question.question}</p>
                        {#if question.user_answer}
                            <p><mark>My answer :</mark> {question.user_answer}</p>
                        {:else}
                            <form on:submit|preventDefault={submitAnswer} id={question.id}>
                                <p><mark>My answer :</mark></p>
                                <textarea id="user_answer" cols="30" rows="10"></textarea>
                                <button type="submit">Envoyer</button>
                            </form>
                        {/if}
                    </div>

                    {#if question.keyword_questions.length > 0}
                        <div class="keyword_questions">
                            <h3>Keyword questions</h3>
                            {#each question.keyword_questions as keyword_question (keyword_question.id)}
                                <div class="keyword_question">
                                    <p><mark>Question :</mark> {keyword_question.question}</p>
                                    {#if keyword_question.user_answer}
                                        <p><mark>My answer :</mark> {keyword_question.user_answer}</p>
                                    {:else}
                                        <form on:submit|preventDefault={submitKeywordAnswer} id={keyword_question.id}>
                                            <p><mark>My answer :</mark></p>
                                            <textarea id="user_answer" cols="30" rows="10"></textarea>
                                            <input type="hidden" name="question-id" value={question.id}>
                                            <button type="submit">Envoyer</button>
                                        </form>
                                    {/if}   
                                </div>
                            {/each}
                        </div>
                    {/if}   
                </section>
            </article>
        {/each}

    {/if}
</div>

<style>
    .container {
        padding: 40px 20vw
    }

    .keyword_question:nth-child(even) { 
        background: #1b2e3c;    
    }

</style>