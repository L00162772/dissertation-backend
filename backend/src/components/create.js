import React, { useState } from 'react';
import { Button, Checkbox, Form } from 'semantic-ui-react'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Create() {
    let navigate = useNavigate();
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [checkbox, setCheckbox] = useState(false);

    const postData = () => {
        axios.post(`https://627c358fe5ac2c452aed2ad9.mockapi.io/fakeData`, {
            firstName,
            lastName,
            checkbox
        }).then(() => {
            navigate('/read')
        })
    }
    return (
        <div> 
            <Form className="create-form">
                <Form.Field>
                    <label>First Name</label>
                    <input type="text" placeholder='First Name' data-testid="firstName" onChange={(e) => setFirstName(e.target.value)}/>
                </Form.Field>
                <Form.Field>
                    <label>Last Name</label>
                    <input type="text" placeholder='Last Name' data-testid="lastName" onChange={(e) => setLastName(e.target.value)}/>
                </Form.Field>
                <Form.Field>
                    <Checkbox label='I agree to the Terms and Conditions' data-testid="terms" onChange={(e) => setCheckbox(!checkbox)}/>
                </Form.Field>
                <Button onClick={postData} data-testid="submit" type='submit'>Submit</Button>
            </Form>
        </div>
    )
}
 