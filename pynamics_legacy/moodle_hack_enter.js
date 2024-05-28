    //let input = ['79.3', '8888.2', 'Type of fertilizer', 'Height of plants.', 'Characteristics or Qualities', 'Numbers or Quantities', 'scientific method', 'Measured in Coulombs and is scalar', '0.000085 kA = 8.5 cA', 'multiply by 100', 'quantitative', 'what is being measured', 'Mass, Charge, Speed, Distance', 'Frequency is measured in Hz, period in s and both quantities are scalars.', 'Acceleration is vector.', 'Work, Energy, Power are scalars.', 'Measured in Amperes and is scalar', 'Measured in Ohms and is scalar', '17.53', 'one', 'mass', 'Weight', '0.003 hm', 'kg·m<sup>2</sup>/s<sup>2</sup>.', 'kg·m<sup>2</sup>/s<sup>3</sup>.', 'kg·m<sup>2</sup>/s<sup>2</sup>.', '<img width="80" height="21" align="bottom" alt="mc…view__U1_Lab__00001_res__mc006-3.jpg" border="0">', 'conclusion', 'm, s, kg, A, K, mol, cd', 'control variable', 'independent variable', 'qualitative and quantitative', 'measured in Volts and is scalar', 'A hypothesis is a testable educated guess.', 'All answers correct.', 'an observation and question', 'Speed and Velocity are measured in m/s.', 'None is correct.', 'Joule', 'Power', null, null]
    // let input = ['an increasing speed', 'AB', 'moving at a constant speed', '40 m', '24 m', '', 'acceleration', '0 m/s', '', 'displacement', 'DE', '', '2 m/s', '11 units', 'could be as small as 2.0 m or as large as 12 m.', '', '40. m', '', 'between the difference and sum of the two magnitudes', 'It maintains a constant velocity.', '<span style="font-size:12pt">T</span>', '0.30 m/s<sup>2</sup>, south', '1.07', '', '', 'The acceleration is downward at all points in the motion.', "The object's velocity is constant.", 'Vx', '0 m', 'The two bricks have exactly the same acceleration.', 'The two bricks have exactly the same acceleration.', 'remains a non-zero constant.', 'moving with constant non-zero acceleration.', 'They hit at the same time.', '13.45 m/s southeast', 'The acceleration is equal to zero.', 'D', 'BC', '60 m', '', null, null]
    
    
let input = ['The size of the force is always exactly the same on both of them.', '394 N', 'The fireman continues to descend, but with constant speed.', '41 N/m', '', '0.11', '55 cm', 'less than 700 N', 'Earth and the satellite feel exactly the same force.', '6.0 N / 0.090 m', '289 N', '28 kg', '0.24', '2.6 m/s<sup>2</sup>', '44 N/m', '', '', 'increase because gravitational force increases.', 'twice as great', '200 N', '0.85 meters', '4.8 m/s', '2 Newtons of force, North, Janice is winning', 'lead ball', 'an object will remain at rest or keep moving in a …ne with constant speed unless a force acts on it.', 'acceleration is calculated by dividing the force e…celeration is in the same direction as the force.', 'Mass is the same, weight is less.', '<img width="8" height="15" align="bottom" alt="mc0…w__U3_Forces__00001_res__mc035-7.jpg" border="0">', '12 kg and 90 kg', 'inertia', '<img width="189" height="26" align="bottom" alt="m…w__U3_Forces__00001_res__mc010-6.jpg" border="0">', '32<i>F</i>', 'If an object exerts a force on another object, the…e and opposite direction back on the first object', '<img width="8" height="15" align="bottom" alt="mc0…w__U3_Forces__00001_res__mc033-7.jpg" border="0">', '69.9 kg', '250 N', 'The cannon moving backward', "Newton's Third Law of Motion", 'There is <i>not</i> a force causing you to slide forward.', 'The wall hits you with a force -10 N.', null, null]
    
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
