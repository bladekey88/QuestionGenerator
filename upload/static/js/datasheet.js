function getQuestions(url) {

    $.getJSON(url, function (data) {
        var items = []
        $.each(data, function (key, val) {
            items.push(val)
        })
        apiOutput = data
		
        $("#info").html("Data Received -  Compiling Questions");
		
		var topics = uniqueTopics(items)
        var topicsTemplate = Handlebars.compile($('#topics-template').html())
        $('#topics').html(topicsTemplate(topics))
        
        displayQuestions()
        
        $('#select-topics').on('change', function () {
            var topic = $(this).val()
            displayQuestions(topic)
            if ($('#exportWord').is(":hidden")) {
                $('#exportWord').show();
                $('#random-button').show();
                $("#random-button").removeClass("invisible")
                $('#exportWord').removeClass("invisible");
            }
        })        
        // // To select api json from dropdown
        $('#select-subject').on('change', function () {
            url = $(this).val()
            getQuestions(url)
        })       
    })
}





// Get unique/distinct from topic array
function uniqueTopics(questions) {
    var set = new Set()
    questions.forEach(function (question) {
        set.add(question.topicid.topicname)
    })
    return Array.from(set)
}



function displayQuestions(topic)
{
    var questions = apiOutput.filter(function (question)
    {
        return (question.topicid.topicname == topic)
    })
    questions = random(questions)
    questions = questions.slice(0, 10)
    var questionTemplate = Handlebars.compile($('#question-template')
        .html())
    $('#questionsInput')
        .html(questionTemplate(questions))
    $('#random-button')
        .on('click', function (e)
        {
            displayQuestions(topic)
            $(this)
                .prop('disabled', true);
            setTimeout(function ()
            {
                $('#random-button')
                    .prop('disabled', false);
            }, 1000);
        })
    results = Array.from(questions)
    $("#info")
        .remove()
    return Array.from(questions)
}

// random function
//Source https://gomakethings.com/how-to-shuffle-an-array-with-vanilla-js/
function random(array)
{
    var currentIndex = array.length
    var temporaryValue, randomIndex;
    // While there remain elements to randomise...
    while (0 !== currentIndex)
    {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }
    return array;
}

