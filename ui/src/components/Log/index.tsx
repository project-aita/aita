import React, { useEffect, useState } from "react";
import Navbar from "../Navbar";
import axios from "axios";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import "./log.scss";

function createData(
  id: number,
  who: string,
  content: string,
  time: string,
) {
  return { id, who, content, time };
}

function Log() {

  // set state for table data rows
  const [rows, setRows] = useState<any[]>([]);

  const getChatHistory = async (): Promise<any[]> => {
  
    try {
      // Send a POST request to the API to retrieve the chat history
      const response = await axios.post('chat_history', {
        model: 'gpt',
      });
  
      return response.data.map((row: any) => {
        // random generated id
        var id = Math.floor(Math.random() * 1000000000);
        var who = row.type;
        var content = row.data.content;
        var time = new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles' });
        return createData(id, who, content, time)
      });
    } catch (err) {
      console.error('Error fetching chat history:', err);
      throw err; // Rethrow the error to reject the Promise
    }
  }

  // Use useEffect to refresh the state when the page loads
  useEffect(() => {
    const refreshState = async () => {
      const newDataArray = await getChatHistory();
      setRows(newDataArray); // Update the state with the new data
    };

    refreshState(); // Call the refreshState function when the component mounts
  }, []); // Empty dependency array to run the effect only once on mount

  
  getChatHistory();
  console.log(rows);

  return (
    <div className="header">
      <div className="header__content">
        <Navbar />
      </div>
      <TableContainer component={Paper}>
      <Table className="log-table" sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Id</TableCell>
            <TableCell align="right">Who</TableCell>
            <TableCell align="right">Content</TableCell>
            <TableCell align="right">Time&nbsp;(PDT)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.id}
              </TableCell>
              <TableCell align="right">{row.who}</TableCell>
              <TableCell align="right">{row.content}</TableCell>
              <TableCell align="right">{row.time}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    </div>
  );
}

export default Log;