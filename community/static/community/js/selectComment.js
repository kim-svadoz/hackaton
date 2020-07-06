const selectButton = document.querySelectorAll('.select-button')
selectButton.forEach(button=>{
    button.addEventListener('click',function(event){
        const articleId=event.target.dataset.id
        console.log(event.target.dataset)
        const commentId=event.target.dataset.comment
        axios.defaults.xsrfCookieName='csrftoken';
        axios.defaults.xsrfHeaderName='X-CSRFToken'
        axios.post(`/community/${articleId}/comment_select/${commentId}`)
        .then(response=>{
            console.log(response.data.likedd)
            if(response.data.likedd){
                event.target.className='fas fa-heart fa-lg select-button'
                event.target.style.color='crimson'
            }else{
                event.target.className='far fa-heart fa-lg select-button'
                event.target.style.color='black'
            }
        })
    })
})