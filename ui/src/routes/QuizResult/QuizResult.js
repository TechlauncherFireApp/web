import './QuizResult.scss';

import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { useHistory } from 'react-router-dom';

const QuizResult = (props) => {
    const [correct, setCorrect] = useState(null);
    const [number, setNumber] = useState(null);
    // const [role, setRole] = useState('');
    const [userAnswers, setUserAnswers] = useState([]);
    const history = useHistory();

    const { solutions, questions, answers } = props;

    const [sequence, setSequence] = useState([]);
    const [correctAns, setCorrectAns] = useState([]);

    useEffect(() => {
        setNumber(questions.length);
        // setRole(roleType);
        setCorrect(solutions.filter(x => x.answer[0].result===true).length);
        setUserAnswers(answers);
        setCorrectAns([...solutions]);
    }, []);

    useEffect(() => {
        setSequence([...Array(number).keys()]);
        console.log(sequence);
    }, [number]);

    // const handleRetakeQuiz = () => {
    //     history.push(`/questions/?roleType=${role}`);
    // }

    const handleReturnMain = () => {
        history.push(`/quiz`);
    }

    return (
        <div className='quiz-result-container'>
            <Container>
                <div>
                    <Row><h1 className='quiz-result-heading'>RESULT</h1></Row>
                    <Row><hr className='quiz-hr'/></Row>
                    <Row sm={2}>
                        <Col><h4 className='quiz-result-txt'>{`You got ${correct} out of ${number} questions correct.`}</h4></Col>
                        <Col className='vertical-line'>
                            {/*<Button className='quiz-result-btn' variant='danger' onClick={() => handleRetakeQuiz()}>Retake quiz</Button>*/}
                            <Button className='quiz-result-btn' variant='danger' onClick={() => handleReturnMain()}>Return to main quiz page</Button>
                        </Col>
                    </Row>
                    <hr/>
                        <Row sm={3}>
                            <Col sm={8}>
                                Questions
                            </Col>
                            <Col sm={2}>
                                Your answer
                            </Col>
                            <Col sm={2}>
                                Solution
                            </Col>
                        </Row>
                        <hr/>
                            {
                                sequence.map((elem) => {
                                    return (
                                        <div key={questions[elem].id}>
                                            <Row sm={3}>
                                            <Col sm={8}>
                                                {questions[elem].description}
                                            </Col>
                                            <Col sm={2}>
                                                {userAnswers[elem]}
                                            </Col>
                                            <Col sm={2}>
                                                {correctAns[elem]?.answer[0].correct}
                                            </Col>
                                            </Row>
                                        </div>
                                    )
                                })
                            }
                </div>
            </Container>
        </div>
    );
};

export default QuizResult;