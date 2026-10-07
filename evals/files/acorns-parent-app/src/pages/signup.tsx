export default function Signup() {
  return (
    <form method="post" action="/api/signup">
      <h1>Create your parent account</h1>
      <input name="fullName" placeholder="Full name" required />
      <input name="nationalIdNumber" placeholder="National ID number" required />
      <input name="phone" placeholder="Phone (07...)" required />
      <input name="email" placeholder="Email" />
      <select name="maritalStatus">
        <option>Married</option><option>Single</option><option>Divorced</option><option>Widowed</option>
      </select>
      <input name="admissionNumber" placeholder="Your child's admission number" required />
      <input name="password" type="password" required />
      <button type="submit">Sign up</button>
    </form>
  );
}
