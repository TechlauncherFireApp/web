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

import { backendPath } from '../../config';
import QuizResult from "../QuizResult/QuizResult";

const QuizQuestions = () => {
    const [questions, setQuestions] = useState([]);
    const [questionNum, setQuestionNum] = useState(0);
    const [answers, setAnswers] = useState(Array(questions.length).fill(null));
    const [progress, setProgress] = useState(0);
    const [solutions, setSolutions] = useState(Array(questions.length).fill(null));
    const [errorMessage, setErrorMessage] = useState("");
    const [role, setRole] = useState('');
    const [completed, setCompleted] = useState(-1);
    const [flag, setFlag] = useState("questions");

    const config = {
            'headers': {
                'withCredentials': true,
                'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Access-Control-Allow-Origin': '*'
            }
        };

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const roleType = urlParams.get('roleType').toLowerCase().replace(/%20/g, " ");
        console.log('This is role type:' + roleType);
        setRole(roleType);

        axios.get(backendPath + `quiz/getRandomQuestion?num=10&role=${roleType}&difficulty=1`, config)
            .then((res) => {
                console.log(res.data);
                setQuestions([...res.data]);
            })
            .catch((err) => {
                console.log(err);
            })
    }, []);

    useEffect(() => {
        const increment = 100 / questions.length;
        setProgress(increment);
    }, [questions]);

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
        setErrorMessage("");
        console.log("questionNum:" + questionNum);
        console.log(completed);
        if (completed === questions.length && questionNum === questions.length - 1) {
            setFlag("results");
        } else if (questionNum === questions.length - 1) {
            setErrorMessage("* You must select and check the answer for all questions to proceed to your results.");
        } else {
            setErrorMessage("");
            const increment = 100 / questions.length;
            setQuestionNum(questionNum + 1);
            setProgress(progress + increment);
        }
    }

    const handleUserInput = (id) => {
        const answersArr = [...answers];
        answersArr[questionNum] = id;
        setAnswers(answersArr)
    }

    const handleCheck = () => {
        let solutionsArr = [...solutions];

        axios.get(backendPath + `quiz/checkMultipleAns?id=${questions[questionNum].id}&ans=${answers[questionNum]}`, config)
            .then((res) => {
                solutionsArr[questionNum] = res.data[0];
                setSolutions(solutionsArr);
            })
            .catch((err) => {
                console.log(err);
            });
    }

    useEffect(() => {
        if (completed !== questions.length) {
            setCompleted(prevState => prevState + 1);
        }
    }, [solutions]);

    return (
        <div className='quiz-question-container'>
            {
                flag === "questions" ?
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
                                        ${solutions[questionNum]?.answer[0].result ? 'correct-solution-box' : 'incorrect-solution-box'} 
                                        ${solutions[questionNum] === undefined ? 'solution-box' : ''}
                                    `}
                                >
                                    {solutions[questionNum]?.answer[0].result ? 'Correct! ' : 'Incorrect'}
                                    <br/>
                                    <br/>
                                    {`${solutions[questionNum]?.answer[0].result ? 'Explanation: ' + solutions[questionNum]?.choice[0].reason : ''}`}
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
                    :
                    <QuizResult roleType={role} questions={questions} solutions={solutions} answers={answers}/>
            }
        </div>
    );
}

export default QuizQuestions;