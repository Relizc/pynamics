    //let input = ['79.3', '8888.2', 'Type of fertilizer', 'Height of plants.', 'Characteristics or Qualities', 'Numbers or Quantities', 'scientific method', 'Measured in Coulombs and is scalar', '0.000085 kA = 8.5 cA', 'multiply by 100', 'quantitative', 'what is being measured', 'Mass, Charge, Speed, Distance', 'Frequency is measured in Hz, period in s and both quantities are scalars.', 'Acceleration is vector.', 'Work, Energy, Power are scalars.', 'Measured in Amperes and is scalar', 'Measured in Ohms and is scalar', '17.53', 'one', 'mass', 'Weight', '0.003 hm', 'kg·m<sup>2</sup>/s<sup>2</sup>.', 'kg·m<sup>2</sup>/s<sup>3</sup>.', 'kg·m<sup>2</sup>/s<sup>2</sup>.', '<img width="80" height="21" align="bottom" alt="mc…view__U1_Lab__00001_res__mc006-3.jpg" border="0">', 'conclusion', 'm, s, kg, A, K, mol, cd', 'control variable', 'independent variable', 'qualitative and quantitative', 'measured in Volts and is scalar', 'A hypothesis is a testable educated guess.', 'All answers correct.', 'an observation and question', 'Speed and Velocity are measured in m/s.', 'None is correct.', 'Joule', 'Power', null, null]
    // let input = ['an increasing speed', 'AB', 'moving at a constant speed', '40 m', '24 m', '', 'acceleration', '0 m/s', '', 'displacement', 'DE', '', '2 m/s', '11 units', 'could be as small as 2.0 m or as large as 12 m.', '', '40. m', '', 'between the difference and sum of the two magnitudes', 'It maintains a constant velocity.', '<span style="font-size:12pt">T</span>', '0.30 m/s<sup>2</sup>, south', '1.07', '', '', 'The acceleration is downward at all points in the motion.', "The object's velocity is constant.", 'Vx', '0 m', 'The two bricks have exactly the same acceleration.', 'The two bricks have exactly the same acceleration.', 'remains a non-zero constant.', 'moving with constant non-zero acceleration.', 'They hit at the same time.', '13.45 m/s southeast', 'The acceleration is equal to zero.', 'D', 'BC', '60 m', '', null, null]
    let input = ['an increasing speed', 'AB', 'moving at a constant speed', '40 m', '24 m', '', 'acceleration', '0 m/s', '', 'displacement', 'DE', '', '2 m/s', '11 units', 'could be as small as 2.0 m or as large as 12 m.', '', '40. m', '', 'the sum of two magnitudes of each vector', 'It maintains a constant velocity.', '<span style="font-size:12pt">T</span>', '0.30 m/s<sup>2</sup>, south', '1.07', '', '', 'The acceleration is downward at all points in the motion.', "The object's velocity is constant.", 'Vx', '0 m', 'The two bricks have exactly the same acceleration.', 'The two bricks have exactly the same acceleration.', 'first decreases and then increases.', 'moving with constant non-zero acceleration.', 'They hit at the same time.', '13.45 m/s southeast', 'The acceleration is equal to zero.', 'D', 'BC', '60 m', '', null, null]
    
    
    let qnum = 0;




    let mainform = document.getElementsByTagName("form")[0]
    let questions = mainform.children[0].children

    for (q of questions) {

            let flag = false;
            let options = q.getElementsByClassName("content")[0].children[0].getElementsByClassName("no-overflow")[0].getElementsByClassName("answer")[0].children

            for (opt of options) {
                let optname;
                try {
                    optname = opt.getElementsByTagName("div")[0].getElementsByTagName("div")[0].children[0].innerHTML
                } catch {
                    optname = opt.getElementsByTagName("div")[0].getElementsByTagName("div")[0].innerHTML
                }

                if (input[qnum].length == 0) {
                    console.warn("Question Number " + (qnum + 1) + " is problomatic. You will have to do that by yourself.")
                    break;
                }

                if (optname == input[qnum]) {
                    opt.getElementsByTagName("input")[0].checked = true
                }
            }



        qnum ++;
    }
