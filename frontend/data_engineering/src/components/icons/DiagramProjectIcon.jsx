const DiagramProjectIcon = ({ size, ...props }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 640 640"
    fill="currentColor"
    width={size}
    height={size}
    {...props}
  >
    <path d="M64 144c0-26.5 21.5-48 48-48h96c26.5 0 48 21.5 48 48v16h128v-16c0-26.5 21.5-48 48-48h96c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48h-96c-26.5 0-48-21.5-48-48v-16H256v16c0 7.3-1.7 14.3-4.6 20.5L320 352h80c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48h-96c-26.5 0-48-21.5-48-48v-96c0-7.3 1.7-14.3 4.6-20.5L192 288h-80c-26.5 0-48-21.5-48-48z" />
  </svg>
);
export default DiagramProjectIcon;