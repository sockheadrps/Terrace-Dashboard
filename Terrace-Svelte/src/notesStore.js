/* eslint-disable max-len */
import { writable } from 'svelte/store';

export const noteListStore = writable([
  {
    id: 1,
    topic: 'Science',
    title: 'Rockets',
    body: 'Bacon ipsum dolor amet tenderloin pork belly capicola, fatback beef ribs ball tip turkey ground round corned beef sirloin venison. Beef shank buffalo pork pork loin ham tri-tip kevin bacon. Hamburger swine ham hock chuck short ribs jerky. Short loin jowl pancetta kielbasa beef beef ribs. Short ribs tongue tenderloin short loin swine venison filet mignon shank pork brisket corned beef pork belly doner. Bresaola strip steak pork chop, brisket tenderloin shoulder pastrami pork doner shankle spare ribs corned beef beef short loin.',
    timeStamp: Date()
  },
  {
    id: 2,
    topic: 'Geography',
    title: 'Volcanos',
    body: 'Bacon ipsum dolor amet tenderloin pork belly capicola, fatback beef ribs ball tip turkey ground round corned beef sirloin venison. Beef shank buffalo pork pork loin ham tri-tip kevin bacon. Hamburger swine ham hock chuck short ribs jerky. Short loin jowl pancetta kielbasa beef beef ribs. Short ribs tongue tenderloin short loin swine venison filet mignon shank pork brisket corned beef pork belly doner. Bresaola strip steak pork chop, brisket tenderloin shoulder pastrami pork doner shankle spare ribs corned beef beef short loin.',
    timeStamp: Date()
  }
]);
