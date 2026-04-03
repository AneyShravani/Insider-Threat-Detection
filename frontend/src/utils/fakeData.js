export function generateUser() {
  return {
    name: "User_" + Math.floor(Math.random() * 100),
    risk: Math.floor(Math.random() * 100)
  };
}