import 'bootstrap/dist/css/bootstrap.min.css';
import './QuizQuestions.scss';

import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import { backendPath } from '../../config';

const QuizQuestions = () => {
    const [questions, setQuestions] = useState([]);
    const [questionNum, setQuestionNum] = useState(0);

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const roleType = urlParams.get('roleType').toLowerCase().replace(/%20/g, " ");
        console.log('This is role type:' + roleType);

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

    const handleClick = () => {
        setQuestionNum(questionNum + 1);
    }

    return (
        <div>
            <Container>
                <Card>
                    <Card.Img variant='top' src='https://www.rbgsyd.nsw.gov.au/getmedia/ce90c9e5-0e81-4904-94c8-5410a143bce7/placeholder_cross_1200x815.png'/>
                    <Card.Body>
                        <Card.Header>
                            <Button variant='secondary' onClick={() => handleClick()}>{questionNum + 1 === questions.length ? 'See result' : 'Next question'}</Button>
                        </Card.Header>
                        <Card.Text>
                            <strong>{ `Question ${questionNum + 1} out of ${questions.length}: ` }</strong>
                            { questions[questionNum]?.description }
                        </Card.Text>
                        <Row xs={1} sm={2}>
                            {
                                questions[questionNum]?.choice.map((elem) => {
                                    return (
                                        <Col key={elem.id}>
                                            <Button variant='danger' className='quiz-answer-btn'>
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
                    </Card.Body>
                </Card>
            </Container>
        </div>
    );
}

export default QuizQuestions;