import 'bootstrap/dist/css/bootstrap.min.css';
import './QuizQuestions.scss';

import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import ProgressBar from 'react-bootstrap/ProgressBar';
import Row from 'react-bootstrap/Row';
import { useHistory } from 'react-router-dom';

import { backendPath } from '../../config';

const QuizQuestions = () => {
    const [questions, setQuestions] = useState([]);
    const [questionNum, setQuestionNum] = useState(0);
    const [answers, setAnswers] = useState(Array(questions.length).fill(null));
    const [progress, setProgress] = useState(10);
    const [solutions, setSolutions] = useState(Array(questions.length).fill(null));
    const [errorMessage, setErrorMessage] = useState("");
    const [role, setRole] = useState('');
    const history = useHistory();

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const roleType = urlParams.get('roleType').toLowerCase().replace(/%20/g, " ");
        console.log('This is role type:' + roleType);
        setRole(roleType);

        const config = {
            'headers': {
                'withCredentials': true,
                'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Access-Control-Allow-Origin': '*'
            }
        };

        // After backend engineers update their work, replace the axios url to: backendPath + `quiz/getRandomQuestion?num=10&role=${roleType}&difficulty=1`

        axios.get(backendPath + `quiz/getRandomQuestion?num=10&role=volunteer&difficulty=1`, config)
            .then((res) => {
                setQuestions([...res.data]);
            })
            .catch((err) => {
                console.log(err);
            })
    }, []);

    useEffect(() => {
        window.onbeforeunload = () => {
            return true;
        };

        return () => {
            window.onbeforeunload = null;
        };
    }, []);

    const handlePrevious = () => {
        setQuestionNum(questionNum - 1);
        const increment = 100 / questions.length;
        setProgress(progress - increment);
        setErrorMessage("");
    }

    const handleNext = () => {
        if (answers[questionNum] === undefined) {
            setErrorMessage("* You must choose an answer and check it!");
        } else if (solutions[questionNum] === undefined) {
            setErrorMessage("* You must check your answer!");
        } else {
            setErrorMessage("");
            setQuestionNum(questionNum + 1);
            if (progress === 100) {
                history.push(`/quiz-result/?correct=${solutions.filter(x => x==="Correct").length}&number=${questions.length}&role=${role}`);
            } else {
                const increment = 100 / questions.length;
                setProgress(progress + increment);
            }
        }
    }

    const handleUserInput = (id) => {
        const answersArr = [...answers];
        answersArr[questionNum] = id;
        setAnswers(answersArr)
    }

    const handleCheck = () => {
        const solutionsArr = [...solutions];
        if (answers[questionNum] === undefined) {
            solutionsArr[questionNum] = "Please choose an answer.";
        } else if (questionNum % 2 === 0) {
            solutionsArr[questionNum] = "An apple is not an orange, so it is not possible to save so many apples in 2 minutes during a fire.";
        } else if (questionNum % 2 !== 0) {
            solutionsArr[questionNum] = "Correct";
        }
        setSolutions(solutionsArr);
    }

    return (
        <div className='quiz-question-container'>
            <Container>
                <Card>
                    <Card.Img variant='top' src='https://www.rbgsyd.nsw.gov.au/getmedia/ce90c9e5-0e81-4904-94c8-5410a143bce7/placeholder_cross_1200x815.png'/>
                    <Card.Body>
                        <Card.Header>
                            <h4><strong>{ `Question ${questionNum + 1} of ${questions.length} ` }</strong></h4>
                            <ProgressBar animated now={progress} variant='dark'/>
                        </Card.Header>
                        <Card.Text>
                            <Row sm={1}>
                                <Col>
                                    <strong>Question: </strong>
                                    { questions[questionNum]?.description }
                                </Col>
                                <Col><Button variant='success' className='check-btn' onClick={() => handleCheck()}>Check answer</Button></Col>
                                <Col
                                    className={`
                                        ${solutions[questionNum] === "Correct" ? 'correct-solution-box' : 'incorrect-solution-box'} 
                                        ${solutions[questionNum] === undefined ? 'solution-box' : ''}
                                    `}
                                >
                                    {solutions[questionNum]}
                                </Col>
                                <Col>Please choose the best answer from one of the following options:</Col>
                            </Row>
                        </Card.Text>
                        <Row xs={1} sm={2}>
                            {
                                questions[questionNum]?.choice.map((elem) => {
                                    return (
                                        <Col key={elem.id}>
                                            <Button variant='danger' className='quiz-answer-btn' onClick={() => handleUserInput(elem.id)}>
                                                <Row>
                                                    <Col className='answer' xs={1}>{elem.id}</Col>
                                                    <Col className='answer' xs={11}>{elem.content}</Col>
                                                </Row>
                                            </Button>
                                        </Col>
                                    )
                                })
                            }
                        </Row>
                        <Card.Footer>
                            <Button variant='secondary' onClick={() => handlePrevious()} className={questionNum === 0 ? 'gone-previous-btn' : 'appear-previous-btn'}>Previous question</Button>
                            <Button variant='secondary' onClick={() => handleNext()} className='next-btn'>{questionNum + 1 === questions.length ? 'See result' : 'Next question'}</Button>
                            <p className='error-message'>{errorMessage}</p>
                        </Card.Footer>
                    </Card.Body>
                </Card>
            </Container>
        </div>
    );
}

export default QuizQuestions;