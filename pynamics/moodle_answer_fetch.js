    let mainform = document.getElementsByTagName("form")[0]
    let questions = mainform.children[0].children

    let answers = []

    for (q of questions) {
        try {
            let flag = false;
            let options = q.getElementsByClassName("content")[0].children[0].getElementsByClassName("no-overflow")[0].getElementsByClassName("answer")[0].children

            for (opt of options) {
                let checked = opt.getElementsByTagName("input")[0].checked
                if (checked) {
                    flag = true;
                    try {
                        answers.push(opt.getElementsByTagName("div")[0].getElementsByTagName("div")[0].children[0].innerHTML)
                    } catch {
                        answers.push(opt.getElementsByTagName("div")[0].getElementsByTagName("div")[0].innerHTML)
                    }
                }
            }

            if (!flag) {
                answers.push(null);
                console.warn("Ignoring question " + q + " because its not filled")
            }
        } catch (err) {
            answers.push(null);
            console.warn("Ignoring question " + q + " because its not a MCQ")
            console.log(err.stack)
        }


    }

    console.log(answers)