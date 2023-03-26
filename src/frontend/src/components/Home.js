import React, { Fragment } from 'react';
import {Button, Table} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Dataset from './Dataset';


function Home(){
    return(
        <Fragment>
            <div style={{margin:"20rem"}}>
                <Table striped bordered hover size="sm">
                    <thread>
                        <tr>
                            <th>
                                Effort:   
                            </th>
                            <th>
                                Description:   
                            </th>
                            <th>
                                Requirement Analysis Hours:   
                            </th>
                            <th>
                                Description Hours:   
                            </th>
                            <th>
                                Coding Hours:   
                            </th>
                            <th>
                                Testing Hours:   
                            </th>
                            <th>
                                Project Management Hours:   
                            </th>
                        </tr>
                    </thread>
                    <tbody>
                        {
                            Dataset && Dataset.length > 0
                            ?
                            Dataset.map((item) => {
                                return(
                                    <tr>
                                        <td>
                                            {item.effort}
                                        </td>
                                        <td>
                                            {item.req_a}
                                        </td>
                                    </tr>
                                )
                            })
                            :
                            "[, , , , , , ]"
                        }
                    </tbody>
                </Table>
            </div>
        </Fragment>
    )
}

export default Home;