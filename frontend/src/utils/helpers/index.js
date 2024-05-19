import {
  LABEL_SHOW_LESS,
  LABEL_SHOW_MORE,
  RESPONSE_ERROR,
  RESPONSE_OK,
  TASKS_PER_PAGE
} from 'utils/constants';

import dayjs from 'dayjs';

export const getFormattedDate = (date) => {
  const dateTime = dayjs(date);
  return dateTime.format('D MMMM YYYY');
};

export const daysBetweenDate = (completedAt, createdAt) => {
  const SECOND = 1000;
  const MINUTE = SECOND * 60;
  const HOUR = MINUTE * 60;
  const DAY = HOUR * 24;
  const diffDays = Math.ceil((completedAt - createdAt) / DAY);
  return diffDays == 1 ? '1 day' : `${diffDays} days`;
};

export const sanitize = (text) => {
  return text.replaceAll(/<\/?[^>]+(>|$)/gi, '').trim();
};

export const validate = (text) => {
  const sanitizedText = sanitize(text);

  if (sanitizedText === '' || !sanitizedText) {
    return { status: RESPONSE_ERROR, message: 'Please enter a valid description' };
  }

  return { status: RESPONSE_OK, text: sanitizedText };
};

export const paginationLabel = (tasks, currentPage) => {
  const indexOfLastTask = currentPage * TASKS_PER_PAGE;
  if (tasks.length < indexOfLastTask) return LABEL_SHOW_LESS;
  return LABEL_SHOW_MORE;
};
